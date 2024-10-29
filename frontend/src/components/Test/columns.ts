import { h } from 'vue';
import { ColumnDef } from '@tanstack/vue-table';

// Define columns for the table
export const columns: ColumnDef<Payment>[] = [
  {
    accessorKey: 'amount',
    header: () => h('div', { class: 'text-right' }, 'Amount'),
    cell: ({ row }) => {
      const amount = Number.parseFloat(row.getValue('amount'));
      const formatted = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      }).format(amount);

      return h('div', { class: 'text-right font-medium' }, formatted);
    },
  },
  // Add other columns as needed
];

interface Payment {
  id: string;
  amount: number;
  status: 'pending' | 'processing' | 'success' | 'failed';
  email: string;
}
