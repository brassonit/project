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
  return <PolicyDoc type="terms" title="이용약관" />
}

export function PrivacyPage() {
  return <PolicyDoc type="privacy" title="개인정보취급방침" />
}
