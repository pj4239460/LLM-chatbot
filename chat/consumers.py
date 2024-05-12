"""
This file contains the WebSocket consumer that will handle the chat messages.
"""
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from openai import OpenAI

class ChatConsumer(AsyncWebsocketConsumer):
    """
    ChatConsumer is a WebSocket consumer that will handle the chat messages.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = None
        # read the OpenAI API key from a file
        with open('openai_key.txt', 'r', encoding="utf-8") as file:
            openai_key = file.readlines()[0].strip()
        # create an OpenAI client
        self.client = OpenAI(api_key=openai_key)

    async def connect(self):
        """
        Called when the socket connects.
        """
        self.messages = []
        await super().connect()

    async def disconnect(self, code):
        """
        Called when the socket disconnects.
        """
        # when the socket disconnects, we can do some cleanup or other actions here

    async def receive(self, text_data=None, bytes_data=None):
        """
        Called when the socket receives a message from the client.
        """
        data = json.loads(text_data)
        self.messages.append(
            {
                "role": "user",
                "content": data['message'],
            }
        )
        # add user validation logic
        if self.validate_user(None):
            # if user is validated, handle the task
            await self.handle_task(self.messages)
        else:
            # if user is not validated, close the connection
            await self.close()

    async def handle_task(self, messages):
        """
        Handle the task by sending the message to OpenAI
        and then sending the response back to the client in chunks.
        """
        # send the message to OpenAI API and get the response
        openai_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,  # tell OpenAI to stream the responses
        )
        # get an iterator from the Stream object
        openai_response_iter = iter(openai_response)

        chunks = []  # collect all the chunks in this list
        # iterate over the iterator
        for chunk in openai_response_iter:
            # add a delay to simulate a real-time chat
            await asyncio.sleep(0.1)
            # get the message from the response
            message_chunk = chunk.choices[0].delta.content if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content else ""

            if message_chunk:  # ensure message_chunk is not empty
                # send the message back to the client
                await self.send(text_data=message_chunk)
                # add the message to the chunks list
                chunks.append(message_chunk)

        # when done, add the system message to our message list
        self.messages.append({
            "role": "system",
            "content": "".join(chunks)
        })
        print("Messages:", self.messages)
        # send a special message to tell the client that the message has been sent,
        # but the connection is still open
        await self.send(text_data=json.dumps({"end_of_message": True}))

    def validate_user(self, user_info):
        """
        Validate the user based on the user information.
        """
        # add user validation logic here
        return True
