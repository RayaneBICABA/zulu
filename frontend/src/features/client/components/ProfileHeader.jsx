import { motion } from "framer-motion";
import { BadgeCheck } from "lucide-react";
import Card from "../../../components/ui/Card";

const ProfileHeader = ({
  name,
  email,
  avatar,
  role = "Client",
}) => {
  return (
    <Card className="text-center">
      <motion.img
        whileHover={{ scale: 1.05 }}
        src={avatar}
        alt={name}
        className="w-24 h-24 rounded-full mx-auto border-4 border-primary-100 shadow-md object-cover"
      />

      <h2 className="mt-4 text-xl font-bold text-secondary-700">
        {name}
      </h2>

      <p className="text-sm text-gray-500 mt-1">
        {email}
      </p>

      <div className="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-50 border border-primary-200">
        <BadgeCheck
          size={16}
          className="text-primary-500"
        />
        <span className="text-sm font-semibold text-primary-600">
          {role}
        </span>
      </div>
    </Card>
  );
};

export default ProfileHeader;