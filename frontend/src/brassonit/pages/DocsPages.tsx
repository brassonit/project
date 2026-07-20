import { useState } from 'react'
import { DOC_VERS, HISTORY, SHOWS, verKo } from '../data'

function VerSelect({ label, value, onChange }: { label: string; value: string; onChange: (v: string) => void }) {
  return (
    <div className="verbox">
      <select
        className="qselect"
        style={{ maxWidth: 320 }}
        value={value}
        onChange={(e) => {
          onChange(e.target.value)
          window.scrollTo(0, 0)
        }}
      >
        {DOC_VERS.map((v) => (
          <option key={v} value={v}>
            {label} ({v})
          </option>
        ))}
      </select>
    </div>
  )
}

export function AboutPage() {
  return (
    <section>
      <div className="docpg">
        <h1 className="doch1">브라소닛 소개</h1>
        <p className="docsub">BRASSONIT — 연예인 섭외대행 · 공연기획</p>
        <h2 className="doch2">회사 소개</h2>
        <p className="docp">
          브라소닛(brassonit)은 연예인 섭외대행과 공연기획을 전문으로 하는 엔터테인먼트 에이전시입니다. 대중가수, 연주자, 강연자, 사회자,
          퍼포먼스 팀까지 300여 팀의 검증된 아티스트 네트워크를 바탕으로 기업 행사, 지역 축제, 대학 행사, 방송 무대에 최적의 라인업을
          제안합니다.
        </p>
        <p className="docp">
          단순 중개를 넘어 행사 기획, 출연 계약, 리허설, 무대 운영까지 전 과정을 원스톱으로 대행하며, 모든 견적 문의에 24시간 이내 회신을
          원칙으로 합니다.
        </p>
        <h2 className="doch2">회사 연혁</h2>
        {HISTORY.map((h) => (
          <div className="fx pfrow" key={h.y}>
            <span className="histy">{h.y}</span>
            <span>{h.t}</span>
          </div>
        ))}
        <h2 className="doch2">주요 기획공연</h2>
        {SHOWS.map((sh) => (
          <div className="fx pfrow" key={sh.title}>
            <span className="histy" style={{ width: 150 }}>
              {sh.date}
            </span>
            <span>
              <b>{sh.title}</b> — {sh.line}
            </span>
          </div>
        ))}
      </div>
    </section>
  )
}

export function TermsPage() {
  const [ver, setVer] = useState(DOC_VERS[0])
  return (
    <section>
      <div className="docpg">
        <h1 className="doch1">이용약관</h1>
        <h2 className="doch2">제1조 (목적)</h2>
        <p className="docp">
          이 약관은 브라소닛(이하 "회사")이 운영하는 연예인 섭외대행 서비스(이하 "서비스")의 이용과 관련하여 회사와 이용자 간의 권리, 의무 및
          책임사항을 규정함을 목적으로 합니다.
        </p>
        <h2 className="doch2">제2조 (정의)</h2>
        <p className="docli">"서비스"란 회사가 제공하는 아티스트 검색, 섭외 견적 문의, 출연 계약 중개 및 공연기획 대행 일체를 말합니다.</p>
        <p className="docli">"이용자"란 이 약관에 따라 서비스를 이용하는 회원 및 비회원을 말합니다.</p>
        <p className="docli">"아티스트"란 회사와 협약을 맺고 서비스에 등록된 가수, 연주자, 강연자, 사회자, 퍼포먼스 팀 등을 말합니다.</p>
        <h2 className="doch2">제3조 (섭외 계약의 성립)</h2>
        <p className="docli">
          이용자의 견적 문의는 청약의 유인이며, 회사가 아티스트 측 확인을 거쳐 출연 조건을 회신하고 이용자가 동의한 때에 계약이 성립합니다.
        </p>
        <p className="docli">출연료, 이동·숙박, 무대·음향 조건 등 세부사항은 개별 계약서에 따릅니다.</p>
        <h2 className="doch2">제4조 (취소 및 환불)</h2>
        <p className="docli">행사일 30일 전 취소 시 계약금 전액 환불, 15일 전 50%, 7일 이내 취소 시 환불이 불가합니다.</p>
        <p className="docli">
          아티스트의 귀책사유(질병, 사고 등)로 출연이 불가한 경우 회사는 동급 아티스트 대체 또는 전액 환불을 제안합니다.
        </p>
        <p className="docli">천재지변 등 불가항력으로 인한 행사 취소 시 양측 협의를 통해 일정 변경 또는 환불을 진행합니다.</p>
        <h2 className="doch2">제5조 (회사의 의무)</h2>
        <p className="docli">회사는 등록 아티스트의 프로필·경력 정보를 성실히 검증하여 제공합니다.</p>
        <p className="docli">회사는 계약된 공연의 정상 진행을 위해 리허설 및 무대 운영을 지원합니다.</p>
        <h2 className="doch2">제6조 (이용자의 의무)</h2>
        <p className="docli">이용자는 견적 문의 시 행사 일시, 장소, 규모 등 정확한 정보를 제공해야 합니다.</p>
        <p className="docli">이용자는 아티스트의 초상권·저작권을 침해하는 무단 촬영·녹음·2차 이용을 할 수 없습니다.</p>
        <h2 className="doch2">제7조 (면책)</h2>
        <p className="docp">
          회사는 이용자와 아티스트 간 개별 합의로 발생한 분쟁, 이용자의 귀책사유로 인한 손해에 대해 책임을 지지 않습니다. 이 약관에 명시되지
          않은 사항은 관련 법령 및 상관례에 따릅니다.
        </p>
        <h2 className="doch2">부칙</h2>
        <p className="docp">이 이용약관은 {verKo(ver)}부터 적용됩니다.</p>
        <VerSelect label="이용약관" value={ver} onChange={setVer} />
      </div>
    </section>
  )
}

export function PrivacyPage() {
  const [ver, setVer] = useState(DOC_VERS[0])
  return (
    <section>
      <div className="docpg">
        <h1 className="doch1">개인정보취급방침</h1>
        <h2 className="doch2">1. 수집하는 개인정보 항목</h2>
        <p className="docli">회원가입 : 이메일, 비밀번호</p>
        <p className="docli">섭외 견적 문의 : 담당자명, 연락처, 소속(회사/단체명), 행사 정보(일시·장소·규모·예산)</p>
        <p className="docli">자동 수집 : 서비스 이용기록, 접속 로그, 쿠키</p>
        <h2 className="doch2">2. 개인정보의 수집 및 이용 목적</h2>
        <p className="docli">회원 식별, 로그인 및 이메일 인증 등 회원 관리</p>
        <p className="docli">아티스트 섭외 견적 산출, 출연 계약 체결 및 이행, 행사 진행 연락</p>
        <p className="docli">좋아요·장바구니 등 맞춤형 서비스 제공, 서비스 개선 통계 분석</p>
        <h2 className="doch2">3. 개인정보의 보유 및 이용 기간</h2>
        <p className="docli">회원 정보 : 회원 탈퇴 시까지 (탈퇴 즉시 파기)</p>
        <p className="docli">계약·결제 기록 : 전자상거래법에 따라 5년</p>
        <p className="docli">소비자 불만·분쟁 처리 기록 : 3년</p>
        <h2 className="doch2">4. 개인정보의 제3자 제공</h2>
        <p className="docp">
          회사는 원칙적으로 이용자의 개인정보를 외부에 제공하지 않습니다. 다만, 섭외 계약 진행에 필요한 최소한의 정보(담당자명, 연락처, 행사
          정보)를 해당 아티스트 소속사에 제공하며, 이용자가 사전에 동의한 경우와 법령에 의한 경우는 예외로 합니다.
        </p>
        <h2 className="doch2">5. 개인정보의 파기 절차 및 방법</h2>
        <p className="docp">
          보유 기간이 경과하거나 처리 목적이 달성된 개인정보는 지체 없이 파기합니다. 전자적 파일은 복구 불가능한 방법으로 삭제하고, 종이
          문서는 분쇄 또는 소각합니다.
        </p>
        <h2 className="doch2">6. 이용자의 권리</h2>
        <p className="docp">
          이용자는 언제든지 자신의 개인정보를 조회·수정·삭제하거나 처리 정지를 요구할 수 있습니다. 관련 문의는 개인정보
          보호책임자(privacy@brassonit.com)에게 연락해 주시기 바랍니다.
        </p>
        <h2 className="doch2">부칙</h2>
        <p className="docp">이 개인정보취급방침은 {verKo(ver)}부터 적용됩니다.</p>
        <VerSelect label="개인정보취급방침" value={ver} onChange={setVer} />
      </div>
    </section>
  )
}
