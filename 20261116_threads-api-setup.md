# Threads API の設定手順（読み取り用）

作成日: 2026-11-16
目的: @roro_sophic の投稿・返信・インサイト（数字）を、パスワードなしで Claude が読めるようにする
範囲: **読み取りだけ**。投稿の権限（threads_content_publish）は入れない（外部への送信はオーナーが確認してから自分で行う、というルールのため）

画面の名前や手順は Meta の公式ドキュメントと解説記事をもとにした目安。最新の画面と違う場合がある。

---

## オーナーがやること

### 1. Meta の開発者アカウントを作る

1. パソコンで https://developers.facebook.com を開く
2. ログインして、開発者として登録する（電話番号などの確認が求められることがある）

### 2. アプリを作る

1. 「マイアプリ」→「アプリを作成」
2. 使い道（ユースケース）で **「Threads API にアクセス」** を選ぶ
3. アプリ名は何でもよい（例：k-threads-reader）

### 3. 権限を選ぶ

ユースケースの設定で、次の3つだけを有効にする。

| 権限 | 用途 |
|---|---|
| threads_basic | 基本（必須） |
| threads_read_replies | 返信を読む |
| threads_manage_insights | 閲覧数・いいねなどの数字を読む |

### 4. 自分を「テスター」にする

1. アプリの「アプリの役割」→「役割」で、**Threads テスター**に @roro_sophic を追加する
2. Threads アプリ側で招待を承認する（設定 → アカウント → ウェブサイトのアクセス許可 → 招待、のような場所。目安）

自分だけが使うなら、テスターのままで使える。Meta の審査（App Review）は、他人のアカウントを扱う場合に必要になる。

### 5. アクセストークンを作る

1. ユースケースの画面にある、トークンを作る機能（「User Token Generator」など）で、@roro_sophic のトークンを作る
2. できたトークンは1時間で切れる短いもの。60日使える長いトークンに交換する
   - 交換はアプリのシークレット（「アプリの設定」→「ベーシック」）を使う
   - 交換のしかたがわからなければ、短いトークンができた時点で教えてくれれば、手順を一緒に確認する

### 6. トークンを Claude に渡す

- **トークンはチャットに貼らない**
- 「トークンができた」と伝えてくれれば、Claude 側から入力フォームを出す。そこに入れると、作業環境に保存され、Claude は中身を見ずに使える

---

## Claude 側でやること（トークンを受け取ったあと）

- 自分の投稿の一覧、本文、日付を読む
- 投稿ごとの数字（閲覧数、いいね、返信、再投稿など）を読む
- 返信を読む（ネタ帳と、悩みの収集に使う）
- `data/post-log.csv` に自動で記録して、週ごとの振り返りを作る

## 注意

- 長いトークンは **60日で切れる**。切れる前に更新が必要（作ってから24時間以上たっていて、まだ切れていないものだけ更新できる）。更新の時期は、近づいたら知らせる
- トークンは、パスワードと同じくらい大事なもの。人に見せない
- 不要になったら、Meta の開発者画面でアプリを削除すれば、トークンも使えなくなる
- API で取れる数字の項目や、取れる期間には制限があり、細かい仕様は未確認

## 参考

- [Meta：Threads API Get Started](https://developers.facebook.com/docs/threads/get-started)
- [Meta：Long-Lived Access Tokens](https://developers.facebook.com/docs/threads/get-started/long-lived-tokens/)
- [Meta：Get Access Tokens and Permissions](https://developers.facebook.com/documentation/threads/get-started/get-access-tokens-and-permissions)
