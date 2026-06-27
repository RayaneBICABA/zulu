import { Heart, MapPin, Star, ChevronRight } from "lucide-react";
import { motion } from "framer-motion";
import Card from "../../../components/ui/Card";

const FavoriteCard = ({
  image,
  name,
  category,
  rating,
  distance,
  onClick,
  onFavorite,
}) => {
  return (
    <motion.div whileTap={{ scale: 0.98 }}>
      <Card
        hoverable
        className="p-0 overflow-hidden cursor-pointer"
        onClick={onClick}
      >
        <div className="flex">
          <img
            src={image}
            alt={name}
            className="w-28 h-28 object-cover"
          />

          <div className="flex-1 p-4 flex flex-col justify-between">
            <div>
              <span className="text-xs font-medium text-primary-600">
                {category}
              </span>

              <h3 className="font-semibold text-secondary-700 mt-1">
                {name}
              </h3>
            </div>

            <div className="flex items-center gap-3 text-sm text-gray-500 mt-3">
              <div className="flex items-center gap-1">
                <Star
                  size={14}
                  className="fill-primary-500 text-primary-500"
                />
                {rating}
              </div>

              <div className="flex items-center gap-1">
                <MapPin size={14} />
                {distance}
              </div>
            </div>
          </div>

          <div className="flex flex-col justify-between p-3">
            <button onClick={onFavorite}>
              <Heart
                size={20}
                className="fill-red-500 text-red-500"
              />
            </button>

            <ChevronRight
              size={20}
              className="text-gray-400"
            />
          </div>
        </div>
      </Card>
    </motion.div>
  );
};

export default FavoriteCard;