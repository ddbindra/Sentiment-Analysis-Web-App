key = "718c0d6938a84500abc1f635dfe64181"
endpoint = "https://survey-text-mining.cognitiveservices.azure.com/"



from flask import Flask
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from flask import Flask, render_template, request

def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

#temp

def sentiment_analysis_example(client, data):

    documents = data #["I had the best day of my life. I wish you were there with me."]
    response = client.analyze_sentiment(documents = documents)[0]
    print("Document Sentiment: {}".format(response.sentiment))
    global temp
    temp = response.confidence_scores
    print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
        response.confidence_scores.positive,
        response.confidence_scores.neutral,
        response.confidence_scores.negative,
    ))
          
#sentiment_analysis_example(client)

#print("temp = {}".format(temp))


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        global email
        email = details['email']
        sentiment_analysis_example(client, [email])
        return render_template('token.html',temp=temp)
    return render_template('index.html')


if __name__ == '__main__':
    app.run()