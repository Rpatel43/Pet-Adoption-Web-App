import React from 'react';
import { Pagination as BsPagination } from 'react-bootstrap';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

/**
 * Simple pagination component displaying page numbers.
 * Highlights the active page and calls onPageChange when a page is clicked.
 */
const Pagination: React.FC<PaginationProps> = ({
  currentPage,
  totalPages,
  onPageChange,
}) => {
  // Generate a list of page items
  const pages = Array.from({ length: totalPages }, (_, i) => i + 1);

  return (
    <BsPagination>
      {pages.map((page) => (
        <BsPagination.Item
          key={page}
          active={page === currentPage}
          onClick={() => onPageChange(page)}
        >
          {page}
        </BsPagination.Item>
      ))}
    </BsPagination>
  );
};

export default Pagination;