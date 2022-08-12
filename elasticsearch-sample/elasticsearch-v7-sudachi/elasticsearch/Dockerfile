FROM arm64v8/openjdk:8-jre-slim as dict_builder

## 辞書の種類の指定(small/core/full)
ARG sudachi_dict_type="core"

## ユーザー辞書ソースを持ってくる
COPY sudachi/custom_dict.txt /home

WORKDIR /home

# Sudachiプラグインのjarファイルを持ってくる (バイナリ辞書の作成のため)
RUN apt update && apt install -y wget unzip \
    && wget https://github.com/WorksApplications/elasticsearch-sudachi/releases/download/v2.1.0/analysis-sudachi-7.17.3-2.1.0.zip \
    && unzip analysis-sudachi-7.17.3-2.1.0.zip \
    # 用意されているシステム辞書を持ってくる
    && wget http://sudachi.s3-website-ap-northeast-1.amazonaws.com/sudachidict/sudachi-dictionary-20220519-${sudachi_dict_type}.zip \
    && unzip sudachi-dictionary-20220519-${sudachi_dict_type}.zip \
    # バイナリ辞書の作成
    && java -Dfile.encoding=UTF-8 -cp /home/sudachi-0.5.1.jar com.worksap.nlp.sudachi.dictionary.UserDictionaryBuilder -o /home/custom.dic -s /home/sudachi-dictionary-20220519/system_${sudachi_dict_type}.dic /home/custom_dict.txt


FROM elasticsearch:7.17.3

ARG sudachi_dict_type="core"

# Sudachiプラグインの設定ファイル
COPY sudachi/sudachi.json /usr/share/elasticsearch/config/sudachi/
# 前ステージでダウンロードしたSudachiのシステム辞書
COPY --from=dict_builder /home/sudachi-dictionary-20220519/system_${sudachi_dict_type}.dic /usr/share/elasticsearch/config/sudachi/
# 前ステージで作ったユーザー辞書
COPY --from=dict_builder /home/custom.dic /usr/share/elasticsearch/config/sudachi/
# 前ステージでダウンロードしたプラグイン
COPY --from=dict_builder /home/analysis-sudachi-7.17.3-2.1.0.zip /usr/share/elasticsearch/

# Sudachiプラグインインストール
# RUN elasticsearch-plugin install file:///usr/share/elasticsearch/analysis-sudachi-7.17.3-2.1.0.zip && \
#     rm /usr/share/elasticsearch/analysis-sudachi-7.17.3-2.1.0.zip
RUN elasticsearch-plugin install file:///usr/share/elasticsearch/analysis-sudachi-7.17.3-2.1.0.zip
