from dataclasses import dataclass, field
from itertools import batched
from typing import Iterable, Iterator, TypeAlias

SomeRemoteData: TypeAlias = int


@dataclass
class Query:
    per_page: int = 3
    page: int = 1


@dataclass
class Page:
    per_page: int = 3
    results: Iterable[SomeRemoteData] = field(default_factory=list)
    next: int | None = None


def request(query: Query) -> Page:
    data = [i for i in range(0, 10)]
    chunks = list(batched(data, query.per_page))
    return Page(
        per_page=query.per_page,
        results=chunks[query.page - 1],
        next=query.page + 1 if query.page < len(chunks) else None,
    )


class RetrieveRemoteData:

    def __init__(self, per_page: int = 3) -> None:
        self.per_page = per_page
        self.current_page = 1
        self.exhausted = False

    def __iter__(self) -> Iterator[SomeRemoteData]:
        while not self.exhausted:
            page = request(Query(per_page=self.per_page, page=self.current_page))
            yield from page.results
            if page.next is None:
                self.exhausted = True
            else:
                self.current_page = page.next


class Fibo:
    def __init__(self, n: int) -> None:
        self.n = n
        self.a = 0
        self.b = 1
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.n:
            raise StopIteration

        result = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return result
