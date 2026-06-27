import { ROUTES } from "../../../constants/routes";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Store } from "lucide-react";

import PageWrapper from "../../../components/layout/PageWrapper";
import Card from "../../../components/ui/Card";
import Button from "../../../components/ui/Button";

import ProfileHeader from "../components/ProfileHeader";
import MenuItem from "../components/MenuItem";

import useAuth from "../../auth/hooks/useAuth";
import { profileMenu } from "../constants/profileMenu";

const ProfilePage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  // Données réelles de l'utilisateur connecté (GET /api/auth/me).
  const profile = {
    name: [user?.first_name, user?.last_name].filter(Boolean).join(" ") || user?.email,
    email: user?.email,
    role: (user?.roles || []).includes("artisan") ? "Artisan" : "Client",
    avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(user?.email || "zulu")}`,
  };

  const handleMenuClick = (item) => {
    if (item.action === "logout") {
      console.log("Logout...");
      return;
    }

    navigate(item.route);
  };

  return (
    <PageWrapper>
      <div className="page-container">
        <div className="page-inner max-w-xl mx-auto px-5 py-8 space-y-6">

          {/* Header */}
          <ProfileHeader
            name={profile.name}
            email={profile.email}
            avatar={profile.avatar}
            role={profile.role}
          />

          {/* Menu */}
          <div className="space-y-4">
            {profileMenu.map((item) => (
              <MenuItem
                key={item.id}
                icon={item.icon}
                title={item.title}
                subtitle={item.subtitle}
                color={item.color}
                onClick={() => handleMenuClick(item)}
              />
            ))}
          </div>

          {/* Become Merchant */}
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <Card className="bg-gradient-to-r from-primary-500 to-primary-600 text-white">

              <div className="flex items-start gap-4">

                <div className="w-14 h-14 rounded-xl bg-white/20 flex items-center justify-center">
                  <Store size={28} />
                </div>

                <div className="flex-1">

                  <h2 className="text-lg font-bold">
                    Devenir Artisan
                  </h2>

                  <p className="text-sm opacity-90 mt-2">
                    Développez votre activité et rendez votre commerce
                    visible auprès de milliers de clients.
                  </p>

                  <Button
                    variant="secondary"
                    className="mt-5"
                    onClick={() => navigate(ROUTES.completeProfile)}
                  >
                    Commencer
                  </Button>

                </div>

              </div>

            </Card>
          </motion.div>

        </div>
      </div>
    </PageWrapper>
  );
};

export default ProfilePage;