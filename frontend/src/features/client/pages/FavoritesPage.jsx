import { ROUTES } from "../../../constants/routes";
import { useState } from "react";
import { ArrowLeft } from "lucide-react";
import { useNavigate } from "react-router-dom";

import PageWrapper from "../../../components/layout/PageWrapper";
import FavoriteCard from "../components/FavoriteCard";
import EmptyFavorites from "../components/EmptyFavorites";

import favoriteService from "../services/favoriteService";

const FavoritesPage = () => {
  const navigate = useNavigate();

  const [favorites, setFavorites] = useState(
    favoriteService.getFavorites()
  );

  const removeFavorite = (id) => {
    setFavorites((prev) =>
      prev.filter((item) => item.id !== id)
    );
  };

  return (
    <PageWrapper>
      <div className="page-container">
        <div className="page-inner max-w-xl mx-auto">

          {/* Header */}

          <div className="flex items-center gap-4 px-5 py-6">

            <button
              onClick={() => navigate(-1)}
              className="w-10 h-10 rounded-xl bg-white shadow border flex items-center justify-center"
            >
              <ArrowLeft size={20} />
            </button>

            <div>
              <h1 className="text-2xl font-bold text-secondary-700">
                Mes favoris
              </h1>

              <p className="text-sm text-gray-500">
                Retrouvez vos commerces préférés
              </p>
            </div>

          </div>

          {/* Liste */}

          <div className="px-5 pb-8 space-y-4">

            {favorites.length === 0 ? (
              <EmptyFavorites
                onExplore={() => navigate(ROUTES.home)}
              />
            ) : (
              favorites.map((favorite) => (
                <FavoriteCard
                  key={favorite.id}
                  {...favorite}
                  onClick={() => console.log(favorite)}
                  onFavorite={() =>
                    removeFavorite(favorite.id)
                  }
                />
              ))
            )}

          </div>

        </div>
      </div>
    </PageWrapper>
  );
};

export default FavoritesPage;