
import fire

from .bm_retrieving import search_dataset
from .bm_retrieving import search
from .bm_indexing import index
from .answering import answer
from .answering import answer_dataset

def main():
    fire.Fire({
        "search": search,
        "search_dataset": search_dataset,
        #"index": load_bm25_index,
        "index" : index,
        "answer" : answer, 
        "answer_dataset": answer_dataset
    })


if __name__ == "__main__":
    main()
