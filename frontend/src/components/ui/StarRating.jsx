import { Star, StarHalf } from 'lucide-react'

const StarRating = ({ rating = 0, count = 0, size = 14 }) => {
  const full = Math.floor(rating)
  const half = rating % 1 >= 0.25 && rating % 1 < 0.75
  const fullAfterHalf = rating % 1 >= 0.75 ? full + 1 : full
  const empty = 5 - fullAfterHalf - (half ? 1 : 0)

  return (
    <div className="flex items-center gap-1">
      <div className="flex items-center">
        {Array.from({ length: fullAfterHalf }).map((_, i) => (
          <Star key={`f${i}`} size={size} className="fill-amber-400 text-amber-400" />
        ))}
        {half && <StarHalf size={size} className="fill-amber-400 text-amber-400" />}
        {Array.from({ length: empty }).map((_, i) => (
          <Star key={`e${i}`} size={size} className="text-gray-200" />
        ))}
      </div>
      {count > 0 && (
        <span className="text-xs text-gray-400 ml-0.5">
          {rating > 0 ? rating.toFixed(1) : '—'} ({count})
        </span>
      )}
    </div>
  )
}

export default StarRating
