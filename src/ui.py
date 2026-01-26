import gradio as gr
from src.rag import get_query_engine

# Initialize query engine lazily
query_engine = None

def get_engine():
    global query_engine
    if query_engine is None:
        query_engine = get_query_engine()
    return query_engine

def query_response(message, history):
    """
    Generator function for the chatbot.
    Returns the updated history with the new message and response.
    """
    if not message:
        return history, ""

    # Initialize history if None
    if history is None:
        history = []

    # Append user message
    history.append({"role": "user", "content": message})
    
    # Add empty assistant message placeholder
    history.append({"role": "assistant", "content": ""})
    
    # Get engine and query
    engine = get_engine()
    streaming_response = engine.query(message)
    
    # Extract sources (available before generation)
    sources = ""
    if streaming_response.source_nodes:
        sources = "\n\n<br><b>Sources:</b><br>"
        for i, node in enumerate(streaming_response.source_nodes):
            metadata = node.metadata
            file_name = metadata.get('file_name', 'Unknown File')
            page_label = metadata.get('page_label', 'Unknown Page')
            snippet = node.node.get_content()[:200] + "..."
            sources += f"{i+1}. <i>{file_name}</i> (Page {page_label})<br><small>{snippet}</small><br><br>"
    
    # Iterate through streaming response
    response_text = ""
    for text in streaming_response.response_gen:
        response_text += text
        # Update last message content
        history[-1]["content"] = response_text + sources
        yield history, ""
        
    return history, "" # Final return

# Custom CSS matching OpenEvidence style
custom_css = """
body {
    background-color: white !important;
}
.gradio-container {
    background-color: white !important;
    max-width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    height: 100vh !important;
    display: flex;
    flex-direction: column;
}
#logo-row {
    padding: 20px;
    text-align: center;
    flex: 0 0 auto;
}
h1 {
    font-family: 'Times New Roman', serif;
    font-size: 2.5em !important;
    color: #333;
    font-weight: 500;
    margin: 0 !important;
}
#chatbot-area {
    flex: 1 1 auto;
    overflow-y: auto;
    border: none !important;
    background: white !important;
    margin-bottom: 20px;
}
.search-container {
    flex: 0 0 auto;
    padding: 20px 10%;
    background: white;
    border-top: 1px solid #eee;
    padding-bottom: 40px;
}
.search-row {
    display: flex;
    align-items: center;
    gap: 10px;
}
#search-input textarea {
    border-radius: 25px;
    border: 1px solid #ddd;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    padding: 12px 20px !important;
    font-size: 1em;
    resize: none; 
}
#search-btn {
    background: #D95D2E !important; 
    color: white !important;
    border-radius: 50%;
    width: 50px !important;
    height: 50px !important;
    min-width: 50px !important; 
    padding: 0 !important;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 5px rgba(217, 93, 46, 0.3);
    border: none;
    font-size: 1.2em;
}
.suggestions-row {
    justify-content: center;
    gap: 10px;
    margin-bottom: 15px;
    flex-wrap: wrap;
}
.suggestion-btn {
    background: #f9f9f9 !important;
    color: #555 !important;
    border: 1px solid #eee !important;
    border-radius: 20px !important;
    padding: 8px 18px !important;
    font-size: 0.9em !important;
    box-shadow: none !important;
    transition: all 0.2s;
}
.suggestion-btn:hover {
    background: #fff !important;
    border-color: #D95D2E !important;
    color: #D95D2E !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
}
"""

def launch_ui():
    with gr.Blocks(title="Medical Retrieval Chatbot", fill_height=True) as demo:
        
        # 1. Header
        with gr.Row(elem_id="logo-row"):
            gr.Markdown("# OpenEvidence")

        # 2. Chat Area (Main Content)
        chatbot = gr.Chatbot(
            elem_id="chatbot-area", 
            show_label=False, 
            avatar_images=(None, None),
            render_markdown=True
        )
        
        # 3. Footer Area (Suggestions + Search)
        with gr.Column(elem_classes="search-container"):
            
            # Suggestions
            with gr.Row(elem_classes="suggestions-row"):
                s1 = gr.Button("Ask for a Quick Fact", elem_classes="suggestion-btn")
                s2 = gr.Button("Ask about Drug Interactions", elem_classes="suggestion-btn")
                s3 = gr.Button("Ask about Guidelines", elem_classes="suggestion-btn")

            # Search Input
            with gr.Row(elem_classes="search-row", equal_height=True):
                user_input = gr.Textbox(
                    placeholder="Ask a medical question...", 
                    show_label=False, 
                    elem_id="search-input",
                    scale=10,
                    max_lines=1,
                    container=False
                )
                submit_btn = gr.Button("➤", elem_id="search-btn", scale=0)

        # 4. Logic
        submit_btn.click(
            fn=query_response,
            inputs=[user_input, chatbot],
            outputs=[chatbot, user_input]
        )
        
        user_input.submit(
            fn=query_response,
            inputs=[user_input, chatbot],
            outputs=[chatbot, user_input]
        )
        
        # Suggestion Buttons - Only update input
        s1.click(lambda: "What is the normal blood pressure range?", None, user_input)
        s2.click(lambda: "Does aspirin interact with ibuprofen?", None, user_input)
        s3.click(lambda: "What are the guidelines for treating Type 2 Diabetes?", None, user_input)

    demo.launch(inbrowser=True, css=custom_css)

if __name__ == "__main__":
    launch_ui()
