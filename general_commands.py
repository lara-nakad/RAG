###Unanswered questions:
#public code_retrieval:
#uv run python -m src search_dataset --dataset_path datasets_public/public/UnansweredQuestions/dataset_code_public.json --k 10 --save_directory data/output/search_results/public/UnansweredQuestions

#public docs_retieval:
#uv run python -m src search_dataset --dataset_path datasets_public/public/UnansweredQuestions/dataset_docs_public.json --k 10 --save_directory data/output/search_results/public/UnansweredQuestions

#to test moulinette for public code/docs for Unanswered questions
#for code
#./moulinette/moulinette-ubuntu evaluate_student_search_results data/output/search_results/public/UnansweredQuestions/dataset_code_public.json datasets_public/public/AnsweredQuestions/dataset_code_public_fixed.json --k 10 --max_context_length 2000

#for docs
#./moulinette/moulinette-ubuntu evaluate_student_search_results data/output/search_results/public/UnansweredQuestions/dataset_docs_public.json datasets_public/public/AnsweredQuestions/dataset_docs_public.json --k 10 --max_context_length 2000

###Answered questions:
#public code_retrieval:
#uv run python -m src search_dataset --dataset_path datasets_public/public/AnsweredQuestions/dataset_code_public.json --k 10 --save_directory data/output/search_results/public/AnsweredQuestions

#public docs_retrieval:
#uv run python -m src search_dataset --dataset_path datasets_public/public/AnsweredQuestions/dataset_docs_public.json --k 10 --save_directory data/output/search_results/public/AnsweredQuestions

##moulinette to test public docs_code for answered questions:
#for code
#./moulinette/moulinette-ubuntu evaluate_student_search_results data/output/search_results/public/AnsweredQuestions/dataset_code_public.json datasets_public/public/AnsweredQuestions/dataset_code_public_fixed.json --k 10 --max_context_length 2000

#for docs
#./moulinette/moulinette-ubuntu evaluate_student_search_results data/output/search_results/public/AnsweredQuestions/dataset_docs_public.json datasets_public/public/AnsweredQuestions/dataset_docs_public.json --k 10 --max_context_length 2000


###private dataset
## Unanswered
### to test docs_code for private unanswered:
#private code retrieval
#uv run python -m src search_dataset --dataset_path datasets_private/private/UnansweredQuestions/dataset_code_private.json --k 10 --save_directory data/output/search_results/private/UnansweredQuestions

#private docs_retrieval
#uv run python -m src search_dataset --dataset_path datasets_private/private/UnansweredQuestions/dataset_docs_private.json --k 10 --save_directory data/output/search_results/private/UnansweredQuestions

#moulinette to test unanswered private code retrieval_docs retrieval
#for code:
#./moulinette/moulinette-ubuntu evaluate_student_search_results data/output/search_results/private/UnansweredQuestions/dataset_code_private.json datasets_private/private/AnsweredQuestions/dataset_code_private.json --k 10 --max_context_length 2000

#for docs:
#./moulinette/moulinette-ubuntu evaluate_student_search_results data/output/search_results/private/UnansweredQuestions/dataset_docs_private.json datasets_private/private/AnsweredQuestions/dataset_docs_private.json --k 10 --max_context_length 2000

#Answered dataset private
#code_retrieval:
#uv run python -m src search_dataset --dataset_path datasets_private/private/AnsweredQuestions/dataset_code_private.json --k 10 --save_directory data/output/search_results/private/AnsweredQuestions

#docs_retrieval:
#uv run python -m src search_dataset --dataset_path datasets_private/private/AnsweredQuestions/dataset_docs_private.json --k 10 --save_directory data/output/search_results/private/AnsweredQuestions

##Moulinette to test docs_code answered:
#code:
#./moulinette/moulinette-ubuntu evaluate_student_search_results data/output/search_results/private/AnsweredQuestions/dataset_code_private.json datasets_private/private/AnsweredQuestions/dataset_code_private.json --k 10 --max_context_length 2000

#docs:
#./moulinette/moulinette-ubuntu evaluate_student_search_results data/output/search_results/private/AnsweredQuestions/dataset_docs_private.json datasets_private/private/AnsweredQuestions/dataset_docs_private.json --k 10 --max_context_length 2000