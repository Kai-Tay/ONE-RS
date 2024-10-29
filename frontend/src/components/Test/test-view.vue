<script setup lang="ts">
import { h, ref } from 'vue'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'

export interface Payment {
  id: string
  amount: number
  status: 'pending' | 'processing' | 'success' | 'failed'
  email: string
}

const data: Payment[] = [
  {
    id: 'm5gr84i9',
    amount: 316,
    status: 'success',
    email: 'ken99@yahoo.com',
  },
  {
    id: '3u1reuv4',
    amount: 242,
    status: 'success',
    email: 'Abe45@gmail.com',
  },
  {
    id: 'derv1ws0',
    amount: 837,
    status: 'processing',
    email: 'Monserrat44@gmail.com',
  },
  {
    id: '5kma53ae',
    amount: 874,
    status: 'success',
    email: 'Silas22@gmail.com',
  },
  {
    id: 'bhqecj4p',
    amount: 721,
    status: 'failed',
    email: 'carmella@hotmail.com',
  },
]

const columns = [
  {
    accessorKey: 'status',
    header: 'Status',
    cell: ({ row }: any) => h('div', { class: 'capitalize' }, row.getValue('status')),
  },
  {
    accessorKey: 'email',
    header: 'Email',
    cell: ({ row }: any) => h('div', { class: 'lowercase' }, row.getValue('email')),
  },
  {
    accessorKey: 'amount',
    header: () => h('div', { class: 'text-right' }, 'Amount'),
    cell: ({ row }: any) => {
      const amount = Number.parseFloat(row.getValue('amount'))

      // Format the amount as a dollar amount
      const formatted = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      }).format(amount)

      return h('div', { class: 'text-right font-medium' }, formatted)
    },
  },
]
</script>

<template>
    <div class="w-full">
      <div class="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead v-for="column in columns" :key="column.accessorKey">
                <!-- Check if header is a function, otherwise display as a string -->
                <div v-if="typeof column.header === 'function'">
                  {{ column.header() }}
                </div>
                <div v-else>
                  {{ column.header }}
                </div>
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <template v-for="row in data" :key="row.id">
              <TableRow>
                <TableCell v-for="column in columns" :key="column.accessorKey">
                  {{ column.cell({ row }) }}
                </TableCell>
              </TableRow>
            </template>
          </TableBody>
        </Table>
      </div>
    </div>
  </template>
  

