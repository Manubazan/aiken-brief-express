import os
import json
import re
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

# Opcional: si el usuario instala openai/tiktoken, podemos usarlos.
try:
    import tiktoken  # type: ignore
except Exception:
    tiktoken = None

@dataclass
class PromptVariant:
    name: str
    system: str
    template: str
    few_shots: Optional[List[Dict[str, str]]] = None
    checklist: Optional[List[str]] = None

def approx_tokens(text: str) -> int:
    """Aproximación de tokens si no hay tiktoken disponible."""
    if tiktoken:
        # Suponemos cl100k_base si está disponible
        try:
            enc = tiktoken.get_encoding("cl100k_base")
        except Exception:
            enc = tiktoken.get_encoding("o200k_base")
        return len(enc.encode(text))
    # fallback: 1 token ≈ 4 chars
    return max(1, int(len(text) / 4))

def estimate_cost(prompt_tokens: int, completion_tokens: int, model_cost: Dict[str, float]) -> float:
    """Calcula costo aproximado: model_cost = {{'prompt': USD/1k_tok, 'completion': USD/1k_tok}}"""
    return (prompt_tokens / 1000) * model_cost.get('prompt', 0.0) + (completion_tokens / 1000) * model_cost.get('completion', 0.0)

def build_messages(variant: PromptVariant, inputs: Dict[str, Any]) -> List[Dict[str, str]]:
    sys_msg = {"role": "system", "content": variant.system}
    # Ejemplos (few-shots) como pares usuario/asistente (breves)
    shots = []
    if variant.few_shots:
        for ex in variant.few_shots:
            shots.append({"role": "user", "content": ex["user"]})
            shots.append({"role": "assistant", "content": ex["assistant"]})
    # Prompt final
    user = variant.template.format(**inputs)
    return [sys_msg] + shots + [{"role": "user", "content": user}]

def mock_model_response(messages: List[Dict[str, str]], checklist: Optional[List[str]]=None) -> Dict[str, Any]:
    """Simula una respuesta JSON con campos clave; útil para demo sin API key."""
    user = [m for m in messages if m["role"] == "user"][-1]["content"]
    # extraer campos simples por regex
    destino = re.findall(r"destino:\s*(.*)", user, flags=re.I)
    destino = destino[0] if destino else "Destino"
    fechas = re.findall(r"fechas desde (.*) hasta (.*)", user, flags=re.I)
    if fechas:
        desde, hasta = fechas[0]
    else:
        desde, hasta = "YYYY-MM-DD", "YYYY-MM-DD"
    pasajeros = re.findall(r"adultos:\s*(\d+).*?menores:\s*(\d+)", user, flags=re.I | re.S)
    if pasajeros:
        ad, mn = pasajeros[0]
    else:
        ad, mn = "2", "0"
    presupuesto = re.findall(r"presupuesto:\s*(\d+)", user, flags=re.I)
    presupuesto = presupuesto[0] if presupuesto else "N/D"

    salida = {
        "itinerario_resumido": f"Día 1-7 en {destino}. Actividades balanceadas (city tour, playa, libre). Ventana: {desde} a {hasta}.",
        "mensaje_whatsapp": f"¡Hola! Te paso una propuesta inicial para {destino} ({desde}↔{hasta}) para {ad} adultos y {mn} menores. ¿Querés que coticemos con desayuno y cerca de la playa?",
        "hoteldo_filtros": {
            "destino": destino,
            "fecha_desde": desde,
            "fecha_hasta": hasta,
            "adultos": int(ad),
            "menores": int(mn),
            "categoria": "3-4*",
            "desayuno": True
        },
        "checks": []
    }
    # aplicar checklist simple
    if checklist:
        for c in checklist:
            ok = "OK" if re.search(c, json.dumps(salida), flags=re.I) else "FALTA"
            salida["checks"].append({c: ok})
    return salida

def run_variant(variant: PromptVariant, inputs: Dict[str, Any], model_cost: Dict[str, float]) -> Dict[str, Any]:
    messages = build_messages(variant, inputs)
    # costo prompt (aprox.)
    prompt_text = " ".join([m["content"] for m in messages])
    ptoks = approx_tokens(prompt_text)

    # Si hay API KEY, el usuario puede reemplazar este mock por una llamada real.
    # Aquí usamos el mock por defecto para que la POC sea 100% ejecutable.
    output = mock_model_response(messages, checklist=variant.checklist)
    completion_text = json.dumps(output, ensure_ascii=False)
    ctoks = approx_tokens(completion_text)

    return {
        "variant": variant.name,
        "prompt_tokens": ptoks,
        "completion_tokens": ctoks,
        "cost_usd_est": estimate_cost(ptoks, ctoks, model_cost),
        "output": output,
        "messages": messages
    }

def coverage_score(result: Dict[str, Any]) -> float:
    """Heurística simple: penaliza si faltan campos clave y longitud extrema."""
    out = result["output"]
    base = 0.0
    # Campos requeridos
    required = ["itinerario_resumido", "mensaje_whatsapp", "hoteldo_filtros"]
    base += sum(1 for k in required if k in out)
    # Penalización si falta destino o fechas
    hd = out.get("hoteldo_filtros", {})
    if all(hd.get(x) for x in ["destino", "fecha_desde", "fecha_hasta"]):
        base += 1
    # Bonus si checklist todo OK
    checks = out.get("checks", [])
    if checks and all(list(d.values())[0] == "OK" for d in checks):
        base += 1
    return base  # máx 5

