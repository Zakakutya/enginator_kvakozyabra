

from flask import Flask, render_template, request, jsonify
from markupsafe import Markup
import openai
import textwrap

# Set OpenAI API key
openai.api_key = "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"


# prompt1 is a prompt for the first paragraph
prompt1 = """
   write an approximately 30 word text (no more than 30) for dictation with fixed control text to transcribe for the topic: describes a modern trendsetter's proposal to incorporate the spirit of a cultural icon, Artur Alliksaare, into the annual Song and Dance Party in Estonia. The suggestion is to start the celebration with some popular music pieces that reflect Alliksaare's essence on the occasion of his centenary birth.

    The difficulty of this text should be moderated. 

    Linked words: Artur Alliksaare (Estonian poet), centenary (100th anniversary), popular music (music that is popular with the public), Facebook.

    The amount of complex words is low. There are no words that are particularly difficult to understand or pronounce.
"""
# prompt2 is a prompt for the second paragraph
prompt2 = """
    write an approximately 30 word text (no more then 30, but it can be less) for dictation with fixed control text to transcribe with the purpose: the paragraph appears to be to suggest a humorous idea or scenario involving a joint choir and a "Kindmeelse looma kimbatus kingapoes" song title. 

There are a few linking words used in the sentence to connect the clauses and ideas. "If" is used to introduce the subordinate clause and indicate a condition. "With" is used to introduce the object of the preposition. 

The difficulty of this text should be moderated. 

Keywords: joint choir, year of movement, pronunciation exercise, song, Kindmeelse looma kimbatus kingapoes.

In terms of complex words, there are a few words that may be considered complex or specialized, such as "pronunciation”. """

#prompt3 is a prompt for the third paragraph
prompt3 = """
    write an approximately 30 word text (no more then 30, but it can be less) for dictation with fixed control text to transcribe with the the main idea of the paragraph is to provide information about the song "Koit" by Mihkel Lüdig, which is currently used as a popular choice for singing parties. The paragraph briefly mentions the history of the song, stating that the lyrics were reportedly written by Friedrich Kuhlbars in a short amount of time while in the singing group Koit. The purpose of the paragraph is to give context to the song's popularity and provide some historical background on its creation.
    The difficulty of this text should be moderated.
    Keywords: singing parties, song, Koit, Mihkel Lüdig, Friedrich Kuhlbars, quarter of an hour, fire.

    """

#prompt4 is a prompt for the fourth paragraph
prompt4 = """
   write an approximately 30 word text (no more then 30, but it can be less) for dictation with fixed control text to transcribe with the the main idea of the paragraph is to provide: The main idea of this paragraph is the origin of the name and idea for a society, which was conceived in a tavern near Võrtsjärve. The purpose of the paragraph is to provide background information on the circumstances under which the society's name and idea were created, specifically, that it was in a tavern and with the company of song celebrants who had been drinking summer booze and witnessed the sunrise in the east.

    The difficulty of this text should be moderated.

    Keywords: creating, society, name, tavern, Võrtsjärve, song celebrants, summer booze, red dawn, eastern sky.


"""

#prompt5 is a prompt for the fifth paragraph
prompt5 = """ 
   write an approximately 30 word text (no more then 30, but it can be less) for dictation with fixed control text to transcribe with the main idea and purpose: The main idea of the paragraph is that the poetry of Alliksaare is not commonly known or widely read. The purpose of the paragraph is to mention the title of a posthumously published collection of Alliksaare's poetry, which is "Non-existence could also be absent." The paragraph implies that this collection may be worth exploring despite the poet's relative obscurity.

The difficulty of this text should be moderated.

Keywords: Alliksaare, poetry, repertoire, Non-existence could also be absent, title, posthumously published, poetry collection."""

app = Flask(__name__)
# function to get response to a prompt from chatGPT API
def getResponse(prompt):
    # Send the prompt to the API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()
# function to format the response from chatGPT API into 80 character per line
def format_message(message):
    wrapped_message = textwrap.fill(message, width=80)
    formatted_message = "<p>" + wrapped_message.replace("\n", "<br>") + "</p>"
    return formatted_message

# function to start the web app
@app.route('/')
def index():
    return render_template('web.html')

# function to get data from the web app and send it back to the web page
@app.route('/data', methods=['POST'])
def data():
    message = " "
    # if the connection is successful, get the response from the API and format it
    try:
        message = format_message(getResponse(prompt1))
        message += "<br><br>"
        message += format_message(getResponse(prompt2))
        message += "<br><br>"
        message += format_message(getResponse(prompt3))
        message += "<br><br>"
        message += format_message(getResponse(prompt4))
        message += "<br><br>"
        message += format_message(getResponse(prompt5))
    # if the connection is not successful, send an error message
    except:
        message = "Error: Connection to OpenAI API failed."
    
    return jsonify({'message': Markup(message)})

if __name__ == '__main__':
    app.run(debug=True)


