# はじめての同期ガイド

このメモは、Codex・GitHub Desktop・GitHub の関係を確認するための手順です。

## 3つの役割

- Codex：ファイルを作る、文章やコードを直す
- GitHub Desktop：変更を保存してGitHubに送る、GitHubから取り込む
- GitHub：2台のPCで共有する置き場所

## GitHubからこのPCへ取り込む

1. GitHub Desktopを開く
2. 左上が `codex-practice` になっていることを確認する
3. `Fetch origin` を押す
4. `Pull origin` が表示されたら押す
5. `Show in Finder` を押す
6. `index.html` が見えたら成功

## このPCからGitHubへ送る

1. CodexやFinderでファイルを変更する
2. GitHub Desktopを見る
3. 左側に変更ファイルが出る
4. 下の `Summary` に短い説明を書く
5. `Commit to main` を押す
6. `Push origin` を押す

## よくある表示

### No local changes

これは「中身が空」という意味ではありません。

「今は保存待ちの変更がない」という意味です。

### Fetch origin

GitHubに新しい変更があるか確認するボタンです。

### Pull origin

GitHubにある新しい変更を、このPCへ取り込むボタンです。

### Push origin

このPCで保存した変更を、GitHubへ送るボタンです。

## 迷ったら

まず GitHub Desktop で `Fetch origin` を押します。

そのあと `Pull origin` が出たら押します。

中身を見たいときは `Show in Finder` を押します。
