"""Convert model objects to structure."""
from typing import Any, Callable, Dict, List, Sequence


MODEL_METADATA = {
    'author': ('__author__', ''),
    'date': ('__date__', ''),
    'version': ('__version__', ''),
}


def marshal_particle(particle: object) -> Dict[str, Any]:
  """Marshal particle objects."""
  result: Dict[str, Any] = marshal_default(particle)
  result['name'] = str(particle)
  result['slug'] = repr(particle)
  result['line_type'] = particle.find_line_type()
  return result

def marshal_order(order: object) -> Dict[str, Any]:
  """Marshal CouplingOrder objects."""
  result: Dict[str, Any] = {}
  result['name'] = order.name
  result['expansion_order'] = order.expansion_order
  result['hierarchy'] = order.hierarchy
  result['perturbative_expansion'] = order.perturbative_expansion
  return result

def marshal_function(func: object) -> Dict[str, Any]:
  """Marshal CouplingOrder objects."""
  result: Dict[str, Any] = {}
  result['name'] = func.name
  result['arguments'] = func.arguments
  result['expr'] = func.expr
  return result

def marshal_list(
    things: List[Any],
    marshal_fn: Callable[[object], Dict[str, Any]],
) -> List[Dict[str, Any]]:
  """Marshal object list."""
  return [
    marshal_fn(thing)
    for thing in things
  ]

def marshal_default(thing: object) -> Dict[str, Any]:
  """Marshal other objects."""
  result: Dict[str, Any] = {}
  for name, value in thing.get_all().items():
    if value is None or name.startswith('_'):
      continue
    result[name] = value
  return result

MODEL_FIELDS = {
  'all_particles': marshal_particle,
  'all_vertices': marshal_default,
  'all_couplings': marshal_default,
  'all_lorentz': marshal_default,
  'all_parameters': marshal_default,
  'all_orders': marshal_order,
  'all_functions': marshal_function,
  'all_propagators': marshal_default,
  'all_decays': marshal_default,
  'all_form_factors': marshal_default,
  'all_CTvertices': marshal_default,
  'all_CTparameters': marshal_default,
}

def marshal_model(model: object) -> Dict[str, Any]:
  """Marshal model object."""
  result: Dict[str, Any] = {}
  for key, (attr, dflt) in MODEL_METADATA.items():
    result[key] = getattr(model, attr, dflt)

  for attr, marshal_fn in MODEL_FIELDS.items():
    value_list = getattr(model, attr, None)
    if value_list is None:
      continue
    result[attr] = marshal_list(value_list, marshal_fn)
  return result
