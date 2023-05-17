# //         all dependencies i have imported from  given reference code //
from langchain.document_loaders import PyPDFLoader 
from langchain.embeddings import OpenAIEmbeddings 
from langchain.vectorstores import Chroma 
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI


from django.shortcuts import render
import os
from django.core.files.storage import FileSystemStorage
from django.views.generic import View


class InteractWithPdf(View):
	template_name = 'content.html' 

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context


	def post(self, request):
		os.environ['OPENAI_API_KEY'] = "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"

		if request.FILES['pdf_input']:
			pdf_input = request.FILES['pdf_input']
			file_system = FileSystemStorage()
			input_filename = file_system.save(pdf_input.name, pdf_input)
			file_path_of_pdf = file_system.path(input_filename)
			loader = PyPDFLoader(file_path_of_pdf)
			pages = loader.load_and_split()
			embeddings = OpenAIEmbeddings(chunk_size=1)
			vectordb = Chroma.from_documents(pages, embedding=embeddings, persist_directory=".")
			vectordb.persist()
			memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
			pdf_qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0.9), vectordb.as_retriever(), memory=memory)
			input_question = "What are the 2 main types of testing?"
			output = pdf_qa({"question": input_question})
		return render(request, 'content.html', {'asked_question':output['question'], 'answer':output['answer']})


