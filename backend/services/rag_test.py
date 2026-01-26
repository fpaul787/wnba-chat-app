from simple_rag_service import SimpleRagService

rag_service = SimpleRagService()
query = "Who is Angel Reese?"
answer = rag_service.generate_answer(query)
print("Answer:", answer)