des = {
    'version': "1.0.0",
    'credits': "Soiz",
    'description': "Lệnh mẫu"
}

def handle_example_command(message, message_object, thread_id, thread_type, author_id, client):
    #thay thế logic của bạn
    client.replyMessage(Message(text="Đây là lệnh ví dụ!"), message_object, thread_id, thread_type)

def get_szl():
    return{
        "example":handle_example_command
    }