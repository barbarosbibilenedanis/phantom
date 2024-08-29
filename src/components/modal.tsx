import * as React from "react";
import { MdInfo } from "react-icons/md";
import { Link, Navigate, NavLink } from "react-router-dom";
import { FaRegTimesCircle } from "react-icons/fa";

export interface ModalProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  isOpen: boolean;
  children?: React.ReactNode;
  closeFunc: any;
}

const Modal = ({ isOpen, children, closeFunc }: ModalProps) => {
  return (
    <>
      {isOpen && (
        <div className="fixed inset-0 z-40 backdrop-blur-sm">
          <div className="w-full justify-end p-5 absolute z-50 flex">
            <FaRegTimesCircle
              onClick={closeFunc}
              className="text-4xl text-white"
            />
          </div>
          <div className="flex  items-center h-full w-full max-w-full justify-center">
            {children}
          </div>
        </div>
      )}
    </>
  );
};

export default Modal;
