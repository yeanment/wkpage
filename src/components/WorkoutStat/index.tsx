import { intComma } from '@/utils/utils';
import { MAIN_COLOR } from '@/utils/const';

const WorkoutStat = ({
  value,
  description,
  pace,
  className,
  distance,
  onClick,
  color = MAIN_COLOR,
}: {
  value: string;
  description: string;
  pace: string;
  className: string;
  distance: string;
  onClick: (_year: string) => void;
  color: string;
}) => (
  <div
    className={`${className || ' '} w-100 pb-2`}
    onClick={onClick}
    style={{ color: color }}
  >
    <span className={`text-5xl font-bold italic`}>{intComma(value)}</span>
    <span className="text-2xl font-semibold italic">{description}</span>
    {pace && <span className="text-5xl font-bold italic">{' ' + pace}</span>}
    {pace && <span className="text-2xl font-semibold italic"> Pace</span>}

    {distance && (
      <span className="text-5xl font-bold italic">{' ' + distance}</span>
    )}
    {distance && <span className="text-2xl font-semibold italic"> KM</span>}
  </div>
);

export default WorkoutStat;
