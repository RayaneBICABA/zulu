import { ChevronRight } from "lucide-react";
import { motion } from "framer-motion";
import Card from "../../../components/ui/Card";

const MenuItem = ({
  icon: Icon,
  title,
  subtitle,
  onClick,
  color = "text-primary-500",
}) => {
  return (
    <motion.div whileTap={{ scale: 0.98 }} onClick={onClick}>
      <Card
        hoverable
        className="flex items-center justify-between cursor-pointer"
      >
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-primary-50 flex items-center justify-center">
            <Icon size={22} className={color} />
          </div>

          <div>
            <h3 className="font-semibold text-secondary-700">
              {title}
            </h3>

            {subtitle && (
              <p className="text-sm text-gray-500 mt-1">
                {subtitle}
              </p>
            )}
          </div>
        </div>

        <ChevronRight
          size={20}
          className="text-gray-400"
        />
      </Card>
    </motion.div>
  );
};

export default MenuItem;