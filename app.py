import imp
import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from data import *
from color import *
from intro import *
import marketing

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(
    'DSPq4+mSO2Yj6K2eNokHxEDzjepfijEkXzfll4ABu6eRzyBPJaKTWRDJ4TI6XHUQcI6VXEHNa3MFsE2oWmrRqz7ELyTEQNJpNkk33lrhoqKXUiiPF4ICI4eAuEEavjyNC1zYrEa/M1k/fI7clJshqgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('f3e25a34be769e4661758d0473c4424d')

# 監聽所有來自 /callback 的 Post Request


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "Tukey介紹":
        content = intro()
        link = "https://www.youtube.com/watch?v=xGraOmZhw1s"
        message = [TextSendMessage(text=content), TextSendMessage(text=link)]
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    if event.message.text == "風力發電性能監控":
        content = get_predicted_value()
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    if event.message.text == "銀行定存客戶購買機率預測":
        content = marketing.get_predicted_value()
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    if event.message.text == "Tukey試用":
        buttons_template = TemplateSendMessage(
            alt_text='您部署的模型',
            template=ButtonsTemplate(
                title='您部署的模型',
                text='請選擇',
                thumbnail_image_url='https://img.onl/NN5ngA',
                actions=[
                    MessageTemplateAction(
                        label='最佳化製程預測',
                        text='最佳化製程預測'
                    ),
                    MessageTemplateAction(
                        label='風力發電性能監控',
                        text='風力發電性能監控'
                    ),
                    MessageTemplateAction(
                        label='銀行定存客戶購買機率預測',
                        text='銀行定存客戶購買機率預測'
                    )

                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0

    if event.message.text == "資源管理":
        content = "伺服器硬體資源\nCPU使用率：4.1%\n記憶體使用率：32.5%\n儲存空間：87GB可用共127.79GB\n\nTukey使用資訊\n資料集總數：97\n現存資料集：72\n已回收：25\n模型資訊\n模型總數：221\n現存模型：174\n已回收：47"
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    if event.message.text == "模型管理":
        content = "模型：風力發電性能監控\n時間：2022-03-11 14:56\n2184筆2特徵\t預測目標：發電功率\n自變數:風機風速(m/s)\n演算法：GAM\n\tRMSE:120.88\tMAE:79.144\tMAAPE:0.0978\n啓用狀態:啓用中"
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    if event.message.text == "演算法說明":
        message = ImageSendMessage(
            original_content_url='https://img.onl/8uqn0t',
            preview_image_url='https://img.onl/8uqn0t'
        )
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    if event.message.text == "圖表解釋":
        message = ImageSendMessage(
            original_content_url='https://img.onl/bE0uxO',
            preview_image_url='https://img.onl/bE0uxO'
        )
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    if event.message.text == "最佳化製程預測":
        content = "當前製程：處理槽進料\n耗分：486分\n最佳化耗分：396分\n與最佳化製程時差：84分"
        message = [TextSendMessage(text=content), ImageSendMessage(
            original_content_url='https://img.onl/LHrMSv',
            preview_image_url='https://img.onl/LHrMSv'
        )]
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    if event.message.text == "Tukey部落格":
        content = "官方網站：https://chimes.ai/\n官方部落格：https://chimesai.medium.com/\nLinkedIn：https://www.linkedin.com/company/chimes-ai"
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    if event.message.text == "聯絡資訊":
        content = f"如有預約試用、合作洽談、及Tukey的相關問題，歡迎聯絡我們！\n行銷專員 Andy Sheu 許安聖\n電子郵件：ashseu@chimes.ai\n電話：0912490047\n業務經理 Vincent Fan 范文軒\n電子郵件：whfan@chimes.ai\n公司電話：02-77557750 #201"
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    if event.message.text == "我想預約使用Tukey":
        content = "您好，感謝您的回覆！\n預約使用請點選以下連結，填寫您的基本資料，我們將有專人為您服務！\nhttps://forms.gle/cphjEPyhbE1rQFtt9"
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)
    if event.message.text == "Tukey應用場景":
        message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://img.onl/bLI1iF',
                        title='設備異常監控',
                        text='提前預知生產設備性能狀況，達到預防無預警停機。',
                        actions=[
                            URITemplateAction(
                                label='點擊獲得更多資訊',
                                uri='https://chimes.ai/'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://img.onl/CyvYbA',
                        title='製程模擬最佳化',
                        text='自動調控最佳生產參數，在符合交付條件下最小化能源使用。減少能源浪費，降低成本。',
                        actions=[

                            URITemplateAction(
                                label='點擊獲得更多資訊',
                                uri='https://chimes.ai/'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://img.onl/kCiG8H',
                        title='企業ESG應用',
                        text='推動製程低碳轉型、持續節能減碳及擴大產品碳足跡盤查。具體計畫包括深化AI應用、數位轉型等多項措施。',
                        actions=[

                            URITemplateAction(
                                label='點擊獲得更多資訊',
                                uri='https://chimes.ai/'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://img.onl/3T4CxK',
                        title='生產排程需求預測',
                        text='透過過去歷史資料預測下季原料需求量及排程建議，達到零庫存目標並滿足訂單需求。',
                        actions=[

                            URITemplateAction(
                                label='點擊獲得更多資訊',
                                uri='https://chimes.ai/'
                            )
                        ]
                    )
                ]
            )
        )

        line_bot_api.reply_message(event.reply_token, message)
        return 0
    else:
        content = f"如需其他服務，請稍待片刻，本公司會立即為您服務！"
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)
        return 0


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
