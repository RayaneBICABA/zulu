const favoriteService = {
  getFavorites() {
    return [
      {
        id: 1,
        name: "Quincaillerie Brama",
        category: "Quincaillerie",
        rating: 4.8,
        distance: "850 m",
        image:
          "https://images.unsplash.com/photo-1517048676732-d65bc937f952?q=80&w=600",
      },
      {
        id: 2,
        name: "Garage Prestige",
        category: "Mécanique",
        rating: 4.9,
        distance: "1.4 km",
        image:
          "https://images.unsplash.com/photo-1486006920555-c77dcf18193c?q=80&w=600",
      },
    ];
  },
};

export default favoriteService;