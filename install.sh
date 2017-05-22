# GitHubUploaderをインストールする
# -----------------------------------------
# 1. 必要ツールのインストール
# 2. 必要Pythonパッケージのインストール
# 3. 環境変数パスへの登録
# -----------------------------------------

# 1. 必要ツールのインストール
# sqlite3, python3, pip3の存在確認とインストール(apt, apt-getコマンド版)
#   * OSによってパッケージ管理ツールが異なる（Linux(Debain系: apt,apt-get, RedHat系:rpm,yum), Mac(brew), Windows(ない?)）
#   * `apt-get install`, `pip3 install`は管理者権限が必要。（1件ずつパスワード入力が必要）
#     * パスワード入力を自動化できない。visudoで`/etc/sudoers`に`username ALL=(ALL) NOPASSWD: /usr/bin/apt-get`を追記すればいいらしいが微妙
#       * セキュリティ的にどうなのか
#       * visudoインストール強要はどうなのか
#       * visudoのインストールは自動化できない
#   * 以下のコマンドでは自動化できない
#$ dpkg --list sqlite3
#要望=(U)不明/(I)インストール/(R)削除/(P)完全削除/(H)保持
#| 状態=(N)無/(I)インストール済/(C)設定/(U)展開/(F)設定失敗/(H)半インストール/(W)トリガ待ち/(T)トリガ保留
#|/ エラー?=(空欄)無/(R)要再インストール (状態,エラーの大文字=異常)
#||/ 名前           バージョン   アーキテクチ 説明
#+++-==============-============-============-=================================
#ii  sqlite3        3.8.2-1ubunt i386         Command line interface for SQLite
#$ dpkg --list aaaaaaa
#dpkg-query: aaaaaaa に一致するパッケージが見つかりません
#$ dpkg --list python3
#ii  python3        3.4.0-0ubunt i386         interactive high-level object-ori
#$ dpkg --list python3-pip
#ii  python3-pip    1.5.4-1ubunt all          alternative Python package instal
# 上記では存在するか否か機械的に判断できない。文言で判定しても英語だったらアウト。dpkgコマンドがある環境かどうかも不明。
# 以下のコマンドだけでも良さそうだが、パスワード入力が必要。

# sudo apt-get install python3
# sudo apt-get install python3-pip
# sudo apt-get install sqlite3

# 2. 必要Pythonパッケージのインストール
# 
# sudo pip3 install pytz
# sudo pip3 install furl
# sudo pip3 install requests
# sudo pip3 install dataset
# sudo pip3 install PyYAML
# sudo pip3 install bs4

# 3. 環境変数パスへの登録
# 3-1. Pythonの実行コマンドを省略するための記述
which_python3=`which python3`
python_header='#!'$which_python3
echo $python_header
# GitHubUploader.pyをコピーし任意のファイル名にする(hup.py, gip.py, githubup.py, hubup.py, githup.py)
# 上記ファイルの1行目を${python_header}に変更する
# 3-2. このディレクトリをPATHに通す
# 3-3. 初回起動(`$ hup.py`で起動できるはず。マスターDB作成する)

