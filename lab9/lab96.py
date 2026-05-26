from typing import final
@final
class Base:
    pass
# un linter (como MyPy) marcara esto como ERROR:
class Derivada(Base):
    pass    