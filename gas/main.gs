//#####################################################################
//   No-IP から送られてくる更新要求メールを自動処理します。
//     * GASの実行トリガー推奨設定: 時間主導型x30分
//     * V8ランタイム必須
//#####################################################################

// メール本文を投げて実際の処理を行うAPIのURL
const BackendURL = ``;

// 管理対象のドメイン名
const TargetDomainName = "example.com";

// メールに含まれる記述条件 (AND条件/正規表現可)
const TargetMailConditions = [
  { to: "MAILADDRESS" },
  { from: ".*@noip.com$" },
  { subject: "^ACTION REQUIRED.*is Expiring Soon$" },
  { body: "Confirm Hostname" },
  { body: "is expiring soon" },
  { body: "Please confirm your hostname now." },
];


/**
 * エントリーポイント
 */
const NoIpAutoUpdate = () => {
  // No-IP の更新を要求するメールを受信トレイから検索
  const mailThreadsFromNoIp = GmailApp.search("in:inbox from:(@noip.com) subject:(Expiring Soon)");

  // スレッド単位で取れてくる
  let callAPISuccessCount = 0;
  let callAPIFailCount = 0;
  for (const thread of mailThreadsFromNoIp) {
    // メッセージの文面確認
    for (const mail of thread.getMessages()) {
      const mailAttributes = {
        subject: mail.getSubject(),
        body: mail.getBody(),
        from: mail.getFrom(),
        to: mail.getTo(),
      };
      // console.log(mailAttributes);

      let valid = true;

      // 条件にマッチするメールかどうか確認
      for (const condition of TargetMailConditions) {
        const key = Object.keys(condition)[0];
        valid |= mailAttributes[key].match(condition[key]);
        if (!valid) {
          console.log(`D:条件マッチせず: [${key}] が パターン [${condition[key]}] を満たしていない`);
          break;
        }
      }
      if (!valid) {
        // マッチしないメールはスキップ
        continue;
      }

      // このメールをAPIに投げて自動処理を行う
      const options = {
        method: "get",
        contentType: "application/json",
        payload: JSON.stringify({
          message: mailAttributes.body,
        }),
      };
      const response = UrlFetchApp.fetch(BackendURL, options);

      if (response.getResponseCode() === 200) {
        callAPISuccessCount++;
        console.info(`I:${response.getContentText("utf-8")}`);
      } else {
        callAPIFailCount++;
        console.warn(`W:${response.getContentText("utf-8")}`);
      }

      break;
    }
  }

  console.info(`I:DONE. APIコール成功回数=${callAPISuccessCount}, APIコール失敗回数=${callAPIFailCount}`);
}
