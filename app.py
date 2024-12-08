import streamlit as st
from google.oauth2 import service_account
from google.cloud import texttospeech

# Streamlit アプリケーションのタイトルを設定
st.title('音声出力アプリ')

# データ入力セクションの見出しを表示
st.markdown('### データ準備')

# ユーザーがテキストを入力するか、ファイルをアップロードするかを選択するセレクトボックスを表示
input_option = st.selectbox('入力データの選択', ('直接入力', 'テキストファイル'))

# 入力データ変数を初期化
input_data = None

# 入力オプションに応じてテキストデータを取得
if input_option == '直接入力':
    # ユーザーがテキストエリアに直接テキストを入力する場合
    input_data = st.text_area('こちらにテキストを入力して下さい。', 'Cloud Speech-to-Text用のサンプル文になります。')
else:
    # ユーザーがテキストファイルをアップロードする場合
    uploaded_file = st.file_uploader('テキストファイルをアップロードして下さい', ['txt'])
    if uploaded_file is not None:
        # アップロードされたファイルからテキストデータを読み込む
        content = uploaded_file.read()
        input_data = content.decode()

# 入力データが存在する場合
if input_data is not None:
    # 入力データを表示
    st.write('入力データ')
    st.write(input_data)

    # パラメータ設定セクションの見出しを表示
    st.markdown('### パラメータ設定')
    st.subheader('言語と話者の性別選択')

    # 言語を選択するセレクトボックスを表示
    lang = st.selectbox('言語を選択して下さい', ('日本語', '英語'))

    # 話者の性別を選択するセレクトボックスを表示
    gender = st.selectbox('話者の性別を選択して下さい', ('default', 'male', 'female', 'neutral'))

    # 音声合成セクションの見出しを表示
    st.markdown('### 音声合成')
    st.write('こちらの文章で音声ファイルの生成を行いますか？')

    # 音声合成を開始するボタンを表示
    if st.button('開始'):
        # secrets から認証情報を取得
        service_account_info = st.secrets["gcp_service_account"]
        credentials = service_account.Credentials.from_service_account_info(service_account_info)

        # Text-to-Speech API のクライアントを初期化
        client = texttospeech.TextToSpeechClient(credentials=credentials)

        # 音声合成リクエストを構築
        synthesis_input = texttospeech.SynthesisInput(text=input_data)

        # 性別の設定
        gender_type = {
            'default': texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
            'male': texttospeech.SsmlVoiceGender.MALE,
            'female': texttospeech.SsmlVoiceGender.FEMALE,
            'neutral': texttospeech.SsmlVoiceGender.NEUTRAL
        }

        # 言語の設定
        lang_code = {
            '英語': 'en-US',
            '日本語': 'ja-JP'
        }

        # 音声の設定
        voice = texttospeech.VoiceSelectionParams(
            language_code=lang_code[lang],
            ssml_gender=gender_type[gender]
        )

        # オーディオの設定
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        # 音声合成リクエストを送信
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # 音声データを再生
        st.audio(response.audio_content)

