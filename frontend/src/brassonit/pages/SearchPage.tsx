import { useNavigate, useSearchParams } from 'react-router-dom'
import { MENU_ORDER } from '../data'
import { useBrass } from '../store'
import { ArtistCard } from '../components'

export default function SearchPage() {
  const navigate = useNavigate()
  const { artists } = useBrass()
  const [sp] = useSearchParams()
  const q = (sp.get('q') || '').trim()

  const found = artists.filter((a) => q && (a.name.includes(q) || a.desc.includes(q) || a.cat.includes(q) || a.sub.includes(q)))
  const groups = MENU_ORDER.map((cat) => ({ cat, list: found.filter((a) => a.cat === cat) })).filter((g) => g.list.length)

  return (
    <section>
      <div className="fx ac crumb">
        <button onClick={() => navigate('/')}>홈</button>
        <span>›</span>
        <span className="fw6" style={{ color: '#000' }}>
          '{q}' 검색 결과
        </span>
      </div>
      <div className="sect" style={{ paddingTop: 20 }}>
        {groups.length > 0 ? (
          groups.map((g) => (
            <div key={g.cat}>
              <div className="fx jb sechd">
                <h2 className="srchd m0" style={{ border: 0, padding: 0 }}>
                  {g.cat}
                  <span>{g.list.length}팀</span>
                </h2>
              </div>
              <div className="grid5" style={{ marginBottom: 48 }}>
                {g.list.map((a) => (
                  <ArtistCard key={a.id} artist={a} withActions={false} />
                ))}
              </div>
            </div>
          ))
        ) : (
          <div className="empty">검색결과가 없습니다.</div>
        )}
      </div>
    </section>
  )
}
