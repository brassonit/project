import { useEffect, useState } from 'react'
import { fetchPolicy } from '../api'
import { HISTORY, SHOWS } from '../data'

// "2026-01-01" → "2026년 1월 1일"
function isoToKo(iso: string): string {
  const [y, m, d] = iso.split('-')
  return `${parseInt(y, 10)}년 ${parseInt(m, 10)}월 ${parseInt(d, 10)}일`
}

function VerSelect({
  label,
  versions,
  value,
  onChange,
}: {
  label: string
  versions: string[]
  value: string
  onChange: (v: string) => void
}) {
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
        {versions.map((v) => (
          <option key={v} value={v}>
            {label} ({v.replaceAll('-', '.')})
          </option>
        ))}
      </select>
    </div>
  )
}

function PolicyDoc({ type, title }: { type: 'terms' | 'privacy'; title: string }) {
  const [versions, setVersions] = useState<string[]>([])
  const [effectiveDate, setEffectiveDate] = useState('')
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    fetchPolicy(type)
      .then((p) => {
        setVersions(p.versions)
        setEffectiveDate(p.effective_date)
        setContent(p.content)
      })
      .catch(() => setError(true))
      .finally(() => setLoading(false))
  }, [type])

  const changeVersion = (date: string) => {
    setEffectiveDate(date)
    fetchPolicy(type, date)
      .then((p) => setContent(p.content))
      .catch(() => setError(true))
  }

  return (
    <section>
      <div className="docpg">
        <h1 className="doch1">{title}</h1>
        {loading ? (
          <p className="docp">불러오는 중…</p>
        ) : error ? (
          <p className="docp">내용을 불러오지 못했습니다.</p>
        ) : (
          <>
            <div dangerouslySetInnerHTML={{ __html: content }} />
            <h2 className="doch2">부칙</h2>
            <p className="docp">이 {title}은 {isoToKo(effectiveDate)}부터 적용됩니다.</p>
            <VerSelect label={title} versions={versions} value={effectiveDate} onChange={changeVersion} />
          </>
        )}
      </div>
    </section>
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
          2014년에 설립된 브라소닛은 공연 제작 및 기획을 주축으로 성장해 온 공연기획사입니다. 2015년 '브라소닛 빅밴드' 창단을 기점으로
          조수미, 나윤선을 비롯하여 최백호, 양희은, YB(윤도현밴드), 김연자 등과 함께한 콜라보 및 전국 투어로 수준 높은 무대를 선보여
          왔습니다.
        </p>
        <p className="docp">
          재즈에서 출발한 저희의 무대는 이제 대중가수 콘서트와 힙합·밴드·트롯 페스타, 그리고 장르의 경계를 넘나드는 다원예술까지
          넓어졌습니다. 최근 3년 동안 전국의 문예회관과 문화재단, 지역 축제, 교육청 기획공연 등에서 60여 개의 무대를 제작하고
          진행했으며, 올 하반기에도 20여 개의 공연이 이어집니다.
        </p>
        <p className="docp">
          주최사의 기획·일정·예산에 맞춰 출연진을 조합하는 4개의 맞춤형 콘서트 브랜드와 온 가족이 함께 즐기는 다원예술 작품을
          선보이며, 섭외부터 연출, 프로덕션, 현장 진행까지 브라소닛이 한 번에 책임집니다.
        </p>
        <p className="docp">
          아울러 아티스트 및 콘텐츠 매니지먼트를 전문으로 하는 (주)에이엠지이엔티와 문화예술 작품의 배급, 유통 및 컨설팅을 담당하는
          (주)온아트를 자회사로 운영하며 시너지를 내고 있습니다.
        </p>
        <h2 className="doch2">회사 정보</h2>
        <div className="fx pfrow">
          <span className="histy">대표</span>
          <span>천인우 (Inwoo Chun, Daniel)</span>
        </div>
        <div className="fx pfrow">
          <span className="histy">기획팀</span>
          <span>서울특별시 강남구 논현로 132길 13, 4층 4853호</span>
        </div>
        <div className="fx pfrow">
          <span className="histy">제작팀</span>
          <span>서울특별시 강남구 도곡로 84길 6, 지하 1층 24-89호</span>
        </div>
        <div className="fx pfrow">
          <span className="histy">연락처</span>
          <span>010-9054-8209 (Fax. 050-4435-8209) · brassonitent@daum.net</span>
        </div>
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
  return <PolicyDoc type="terms" title="이용약관" />
}

export function PrivacyPage() {
  return <PolicyDoc type="privacy" title="개인정보취급방침" />
}
