import * as React from "react";
import { cn } from "../utils/phantomUtils";
// import { EyeIcon } from "@heroicons/react/24/outline";
// import { EyeClosedIcon } from "@radix-ui/react-icons";

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  labelClassName?: string;
  containerClassName?: string;
  label?: string;
  required?: boolean;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  (
    {
      className,
      containerClassName,
      labelClassName,
      label,
      type,
      required,
      ...props
    },
    ref
  ) => {
    const [showPassword, setShowPassword] = React.useState(false);

    const isPasswordType = type === "password";

    const togglePasswordVisibility = () => {
      setShowPassword((prev) => !prev);
    };

    return (
      <div className={containerClassName}>
        <div className="flex">
          {label && (
            <label
              htmlFor="password"
              className={cn(
                "line-clamp-1 text-sm font-medium leading-6 text-gray-900",
                labelClassName
              )}
            >
              {label}
            </label>
          )}
          {required ? <div className="text-red-600">*</div> : null}
        </div>
        <div className="relative">
          <input
            step="any"
            type={showPassword && isPasswordType ? "text" : type}
            className={cn(
              "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",
              className
            )}
            ref={ref}
            {...props}
          />
          {isPasswordType && (
            <button
              type="button"
              className="absolute inset-y-0 right-0 flex items-center pr-3"
              onClick={togglePasswordVisibility}
            >
              {showPassword ? (
                // <EyeClosedIcon className="h-4 w-4 text-gray-400" />
                <div></div>
              ) : (
                <div></div>
                // <EyeIcon className="h-4 w-4 text-gray-400" />
              )}
            </button>
          )}
        </div>
      </div>
    );
  }
);

Input.displayName = "Input";
export { Input };
