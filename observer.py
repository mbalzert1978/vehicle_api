from __future__ import annotations

import contextlib
from random import randrange
from typing import Protocol


class Observable(Protocol):
    _observers: set[Observer]

    def attach(self, observer: Observer) -> None:
        ...

    def detach(self, observer: Observer) -> None:
        ...

    def notify(self) -> None:
        ...


class Weatherstation(Protocol):
    def get_data(self) -> int:
        ...


class WeatherstationObserver:

    """concrete implementation of the weatherstation interface."""

    def __init__(self) -> None:
        self._observers: set[Observer] = set()
        self._state: int = 0

    def business_logic(self) -> None:
        self._state = randrange(0, 10)
        self.notify()

    def attach(self, observer: Observer) -> None:
        self._observers.add(observer)

    def detach(self, observer: Observer) -> None:
        with contextlib.suppress(KeyError):
            self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def get_data(self) -> int:
        return self._state


class Observer(Protocol):
    def update(self, subject: Observable) -> None:
        ...


class ConcreteWeatherA(Observer):
    def update(self, subject: Weatherstation) -> None:
        if subject.get_data() < 3:
            print('ConcreteObserverA: Reacted to the event')


class ConcreteWeatherB(Observer):
    def update(self, subject: Weatherstation) -> None:
        if subject.get_data() == 0 or subject.get_data() >= 2:
            print('ConcreteObserverB: Reacted to the event')


if __name__ == '__main__':
    subject = WeatherstationObserver()
    observer_a = ConcreteWeatherA()
    observer_b = ConcreteWeatherB()

    subject.attach(observer_a)

    subject.attach(observer_b)

    subject.business_logic()
    subject.business_logic()

    subject.detach(observer_a)

    subject.business_logic()
