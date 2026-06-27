import { ROUTES } from "../../../constants/routes";
import {
  Heart,
  Store,
  Settings,
  LogOut,
} from "lucide-react";

export const profileMenu = [
  {
    id: 1,
    title: "Mes favoris",
    subtitle: "Voir vos commerces favoris",
    icon: Heart,
    route: ROUTES.favorites,
    color: "text-red-500",
  },
  {
    id: 2,
    title: "Devenir Artisan",
    subtitle: "Créer et gérer votre commerce",
    icon: Store,
    route: ROUTES.completeProfile,
    color: "text-primary-500",
  },
  {
    id: 3,
    title: "Paramètres",
    subtitle: "Préférences de l'application",
    icon: Settings,
    route: "/settings",
    color: "text-secondary-600",
  },
  {
    id: 4,
    title: "Déconnexion",
    subtitle: "Se déconnecter de votre compte",
    icon: LogOut,
    action: "logout",
    color: "text-error",
  },
];