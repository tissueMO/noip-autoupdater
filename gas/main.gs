//#####################################################################
//   No-IP ���瑗���Ă���X�V�v�����[���������������܂��B
//     * GAS�̎��s�g���K�[�����ݒ�: ���Ԏ哱�^x30��
//     * V8�����^�C���K�{
//#####################################################################

// ���[���{���𓊂��Ď��ۂ̏������s��API��URL
const BackendURL = ``;

// �Ǘ��Ώۂ̃h���C����
const TargetDomainName = "example.com";

// ���[���Ɋ܂܂��L�q���� (AND����/���K�\����)
const TargetMailConditions = [
  { to: "MAILADDRESS" },
  { from: ".*@noip.com$" },
  { subject: "^ACTION REQUIRED.*is Expiring Soon$" },
  { body: "Confirm Hostname" },
  { body: "is expiring soon" },
  { body: "Please confirm your hostname now." },
];


/**
 * �G���g���[�|�C���g
 */
const NoIpAutoUpdate = () => {
  // No-IP �̍X�V��v�����郁�[������M�g���C���猟��
  const mailThreadsFromNoIp = GmailApp.search("in:inbox from:(@noip.com) subject:(Expiring Soon)");

  // �X���b�h�P�ʂŎ��Ă���
  let callAPISuccessCount = 0;
  let callAPIFailCount = 0;
  for (const thread of mailThreadsFromNoIp) {
    // ���b�Z�[�W�̕��ʊm�F
    for (const mail of thread.getMessages()) {
      const mailAttributes = {
        subject: mail.getSubject(),
        body: mail.getBody(),
        from: mail.getFrom(),
        to: mail.getTo(),
      };
      // console.log(mailAttributes);
  
      let valid = true;
  
      // �����Ƀ}�b�`���郁�[�����ǂ����m�F
      for (const condition of TargetMailConditions) {
        const key = Object.keys(condition)[0];
        valid |= mailAttributes[key].match(condition[key]);
        if (!valid) {
          console.log(`D:�����}�b�`����: [${key}] �� �p�^�[�� [${condition[key]}] �𖞂����Ă��Ȃ�`);
          break;
        }
      }
      if (!valid) {
        // �}�b�`���Ȃ����[���̓X�L�b�v
        continue;
      }

      // ���̃��[����API�ɓ����Ď����������s��
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
  
  console.info(`I:DONE. API�R�[��������=${callAPISuccessCount}, API�R�[�����s��=${callAPIFailCount}`);
}
