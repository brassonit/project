import { useNavigate } from 'react-router-dom'
import { useBrass } from '../store'
import { ShowCard } from '../components'

export default function ShowsPage() {
  const navigate = useNavigate()
  const { shows } = useBrass()
  const upcoming = shows.filter((s) => s.upcoming)
  const past = shows.filter((s) => !s.upcoming)
  return (
    <section className="mypg">
      <div className="fx ac crumb">
        <button onClick={() => navigate('/')}>홈</button>
        <span>›</span>
        <span className="fw6" style={{ color: '#000' }}>
          기획공연
        </span>
      </div>
      <h2 className="qsub" style={{ marginTop: 28 }}>
        예정 공연
      </h2>
      <div className="showg">
        {upcoming.map((sh) => (
          <ShowCard key={sh.id} show={sh} />
        ))}
      </div>
      <h2 className="qsub" style={{ marginTop: 48 }}>
        지난 공연
      </h2>
      <div className="showg">
        {past.map((sh) => (
          <ShowCard key={sh.id} show={sh} />
        ))}
      </div>
    </section>
  )
}
