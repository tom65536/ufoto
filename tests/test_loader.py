
from pathlib import Path

from ufoto.loader import load_model
import pytest


def test_loader(model_dir):
  model = load_model(model_dir)
  print(dir(model))
  assert model is not None
  assert 'all_particles' in dir(model)

@pytest.fixture
def model_dir() -> Path:
  model_name = 'MSSMatNLO_UFO'
  root = Path(__file__).parent.parent / 'models' / 'py3'
  return root / model_name
