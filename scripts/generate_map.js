import fs from 'fs';
import Qieyun from 'qieyun';
import { kyonh, tshet as tupa } from 'qieyun-examples';

const kyonh_map = [];
const tupa_map = [];

function* 生成音韻地位() {
    yield* Qieyun.iter音韻地位();
    yield* [
        '幫三庚入',
        '見開三B仙入',
        '端開二庚上',
        '莊侵上',
        '端幽平',
        '日開一歌去',
        '滂咍上',
        '並咍上',
        '透豪去',
        '明三麻平',
        '並一歌上',
        '生合三支上',
        '幫A脂平',
        // 凡韻非幫組
        '溪凡上',
        '徹凡上',
        '溪凡入',
        '徹凡入',
        '孃凡入',
        // 其他需識別地位
        '孃尤平', // 妞
        '端開三麻上', // 嗲
        '曉開齊上', // 徯小韻
        '來開二麻平', // 旯
        '來開三歌上', // 倆
        // 修正音補充地位
        '定開佳上', // 倄
        '滂肴上', // 跑
        '曉開二庚上', // 擤
    ].map((描述) => Qieyun.音韻地位.from描述(描述));
}

const kyonh_override = {
    端幽平: 'ty',
    日開一歌去: 'njah',
    端開三麻上: 'tiax',
};

for (const 音韻地位 of 生成音韻地位()) {
    const { 最簡描述 } = 音韻地位;

    const kyonh_ = kyonh_override[最簡描述] || kyonh(音韻地位);
    // HACK 目前（20220316）版 tshet 需特別處理凡韻非脣音
    // （main 分支已修正，將包含於下版）
    let tupa_;
    if (音韻地位.屬於('凡韻 且 非 脣音')) {
        tupa_ = tupa(Qieyun.音韻地位.from描述(最簡描述.replace('凡', '嚴')));
    } else {
        tupa_ = tupa(音韻地位);
    }

    kyonh_map.push(最簡描述 + '\t' + kyonh_);
    tupa_map.push(最簡描述 + '\t' + tupa_);
}

fs.writeFileSync('cache/kyonh.txt', kyonh_map.join('\n') + '\n');
fs.writeFileSync('cache/tupa.txt', tupa_map.join('\n') + '\n');
