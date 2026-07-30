import { useNavigate } from 'react-router-dom'
import { useBrass } from '../store'
import { ShowCard } from '../components'
import { catIdByName } from '../data'

export default function HomePage() {
  const navigate = useNavigate()
  const { shows, categories } = useBrass()
  const upcoming = shows.filter((s) => s.upcoming)
  return (
    <section>
      {/* 히어로 — CSS로 그린 어두운 무대 씬 (풀블리드, 조명 애니메이션) */}
      <div className="hero herodark">
        <div className="stagefx">
          <div className="beam bm1" />
          <div className="beam bm2" />
          <div className="beam bm3" />
          <div className="stgfloor" />
          <div className="spot sp1" />
          <div className="spot sp2" />
          <div className="haze" />
        </div>
        <div className="posrel heroin">
          <div className="kick">BRASSONIT PRODUCTION</div>
          <h1 className="h1">
            무대를 완성하는
            <br />단 하나의 <em>섭외</em>
          </h1>
          <div className="fx gap12 mt16">
            <button className="bigbtn noshrink" style={{ flex: 'none' }} onClick={() => navigate(`/category/${catIdByName(categories, '대중가수')}`)}>
              아티스트 둘러보기
            </button>
            <button className="bigbtn ghost" style={{ flex: 'none' }} onClick={() => navigate('/quote')}>
              섭외 문의하기
            </button>
          </div>
        </div>
      </div>
      <div className="sect sect0">
        <div className="fx jb sechd" style={{ paddingTop: 24 }}>
          <h2 className="sech2">브라소닛 기획공연</h2>
          <button className="moreb2" onClick={() => navigate('/shows')}>
            더보기 ›
          </button>
        </div>
        <div className="showg">
          {upcoming.map((sh) => (
            <ShowCard key={sh.id} show={sh} />
          ))}
        </div>
      </div>
    </section>
  )
}
