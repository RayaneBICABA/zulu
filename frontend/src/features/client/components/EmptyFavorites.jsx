import { Heart } from "lucide-react";
import Button from "../../../components/ui/Button";

const EmptyFavorites = ({ onExplore }) => {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center">
      <div className="w-20 h-20 rounded-full bg-primary-50 flex items-center justify-center mb-6">
        <Heart
          size={36}
          className="text-primary-500"
        />
      </div>

      <h2 className="text-xl font-bold text-secondary-700">
        Aucun favori
      </h2>

      <p className="text-gray-500 mt-2 max-w-xs">
        Ajoutez vos commerces préférés pour les retrouver rapidement.
      </p>

      <Button
        className="mt-8"
        onClick={onExplore}
      >
        Explorer les commerces
      </Button>
    </div>
  );
};

export default EmptyFavorites;