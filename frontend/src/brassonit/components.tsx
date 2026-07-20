import { useNavigate } from 'react-router-dom'
import type { BrArtist, BrShow } from './data'
import { fmt } from './data'
import { useBrass } from './store'
import { CartIcon, EyeIcon, HeartIcon } from './icons'

export function ShowCard({ show }: { show: BrShow }) {
  const navigate = useNavigate()
  return (
    <button className="showc" onClick={() => navigate(`/shows/${show.id}`)}>
      <div className="simg">
        <img src={show.img} alt={show.title} />
      </div>
      <div className="sdate">{show.date}</div>
      <div className="stitle">{show.title}</div>
      <p className="sline m0">{show.line}</p>
      <div className="fx ac gap12 mt8">
        <span className="fx ac stat">
          <HeartIcon size={14} />
          {fmt(show.likes)}
        </span>
        <span className="fx ac stat">
          <EyeIcon />
          {fmt(show.views)}
        </span>
      </div>
    </button>
  )
}

export function ArtistCard({ artist, withActions = true }: { artist: BrArtist; withActions?: boolean }) {
  const navigate = useNavigate()
  const { liked, carted, toggleLiked, toggleCarted } = useBrass()
  return (
    <div className="acard" onClick={() => navigate(`/artist/${artist.id}`)}>
      <div className="sq posrel">
        <img src={artist.images[0]} alt={artist.name} />
      </div>
      <div className="aname">{artist.name}</div>
      <p className="adesc">{artist.desc}</p>
      {withActions && (
        <div className="fx ac gap12">
          <span className="fx ac stat">
            <HeartIcon size={14} />
            {fmt(artist.likes)}
          </span>
          {/* 모바일(≤620px)에서는 조회수 숨김 */}
          <span className="fx ac stat vstat">
            <EyeIcon />
            {fmt(artist.views)}
          </span>
          <button
            className={`cartb${liked[artist.id] ? ' on' : ''}`}
            title="좋아요"
            onClick={(e) => {
              e.stopPropagation()
              toggleLiked(artist.id)
            }}
          >
            <HeartIcon filled={!!liked[artist.id]} />
          </button>
          <button
            className={`cartb${carted[artist.id] ? ' on' : ''}`}
            style={{ marginLeft: 0 }}
            title="장바구니"
            onClick={(e) => {
              e.stopPropagation()
              toggleCarted(artist.id)
            }}
          >
            <CartIcon size={15} />
          </button>
        </div>
      )}
    </div>
  )
}
