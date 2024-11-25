# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


from dataclasses import dataclass


@dataclass
class ProjectDTO:
    """C'est un data object transfert, il sert à stocker les information
    en mémoire afin de sérialiser plus simplement les données.
    Cela rajoute une couche d'abstraction supplémentaire afin de pouvoir mieux
    découpler le code pouvoir avant de les stocker en base de donnée."""

    project_id: int
    name: str
    path: str
    description: str
    release: str
    visibility: int
    created_at: str
    updated_at: str

    @property
    def project_id(self) -> int:
        return self._project_id

    @project_id.setter
    def project_id(self, value: int) -> str:
        self._project_id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> str:
        self._name = value

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, value: str) -> str:
        self._path = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> str:
        self._description = value

    @property
    def release(self) -> str:
        return self._release

    @release.setter
    def release(self, value: str) -> str:
        self._release = value

    @property
    def visibility(self) -> str:
        return self._visibility

    @visibility.setter
    def visibility(self, value: str) -> str:
        self._visibility = value

    @property
    def created_at(self) -> str:
        return self._created_at

    @created_at.setter
    def created_at(self, value: str) -> str:
        self._created_at = value

    @property
    def updated_at(self) -> str:
        return self._updated_at

    @updated_at.setter
    def updated_at(self, value: str) -> str:
        self._updated_at = value
