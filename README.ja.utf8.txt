紹介

jsonschema はJSON文書がJSON Schema文書構造に従ってるかどうかを検証する
ライブラリです。ライブラリです。JSON Schema Proposal Second Draftの仕様を
基にしています。JSON Schema Proposal Second Draft は以下のURLで参照する
ことができます。

http://groups.google.com/group/json-schema/web/json-schema-proposal---second-draft

インストール

jsonschemaはsetuptoolsを使っているので、adminユーザとして、以下のコマンドで
簡単にインストールすることが出来ます。

python setup.py install

さらに、以下のコマンドを使って、テストを実行することが出来ます。

python setup.py test

使い方

JSONドキュメントとスキーマは検証する前にJSON ParserでPythonの
辞書オブジェクトに変換する必要があります。どのようなJSON Parserを使っても
かまいませんが、ここの例では、simplejsonを使います。

簡単なJSON文書を解析する場合

>>> import jsonschema
>>> jsonschema.validate("simplejson", {"type":"string"})

より複雑なJSON文書を解析する場合

>>> import simplejson
>>> import jsonschema
>>> 
>>> data = simplejson.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
>>> schema = {
...   "type":"array", 
...   "items":[
...     {"type":"string"},
...     {"type":"object",
...      "properties":{
...        "bar":{
...          "items":[
...            {"type":"string"},
...            {"type":"any"},
...            {"type":"number"},
...            {"type":"integer"}
...          ]
...        }
...      }
...    }
...   ]
... }
>>> jsonschema.validate(data,schema)

検証エラーを処理

検証エラーが発生する場合は、ValueErrorと言う例外が起こります。

>>> import jsonschema
>>> try:
...     jsonschema.validate("simplejson", {"type":"string","minLength":15})
... except ValueError, e:
...     print e.message
... 
Length of 'simplejson' must be more than 15.000000

jsonschemaを拡張

simplejsonの様にjsonschemaは拡張できるAPIが提供されています。
JSONSchemaValidatorと言うクラスを拡張すれば、JSON Schema プロパティや、
データ形式を追加することができます。examplesにある例を見てください。

未実装

スキーマリファレンスには対応していません。
unique というプロパティには対応していません。
