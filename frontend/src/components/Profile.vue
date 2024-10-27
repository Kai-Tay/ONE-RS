<template>
    <div class="container mx-auto py-8 max-w-4xl">
        <Card>
            <CardHeader>
                <CardTitle class="text-center">Edit Profile</CardTitle>
            </CardHeader>

            <CardContent>
                <div v-if="loading" class="flex items-center justify-center p-8">
                    <Loader2 class="h-8 w-8 animate-spin" />
                </div>

                <div v-else class="space-y-6">

                    <div class="space-y-6">
                        <div class="flex items-center justify-between">
                            <div>
                                <h3 class="text-lg font-medium">Business Information</h3>
                                <p class="text-sm text-gray-500">
                                    {{ profileData.userType === 'restaurant' ? 'Restaurant Owner' : 'Supplier' }}
                                </p>
                            </div>
                        </div>

                        <div class="space-y-2">
                            <Label for="companyName">Company Name</Label>
                            <Input id="companyName" v-model="profileData.companyName" :disabled="saving"
                                :placeholder="profileData.companyName || 'Enter company name...'" />
                        </div>

                        <div v-if="profileData.userType === 'supplier'" class="space-y-2">
                            <Label for="companyDescription">Company Description</Label>
                            <Textarea id="companyDescription" v-model="profileData.companyDescription" rows="4"
                                :disabled="saving"
                                :placeholder="profileData.companyDescription || 'Describe your business...'" />
                        </div>
                    </div>

                    <Button type="submit" class="w-full" :disabled="saving" @click="handleSubmit">
                        <template v-if="saving">
                            <Loader2 class="mr-2 h-4 w-4 animate-spin" />
                            Saving...
                        </template>
                        <template v-else>
                            Save Changes
                        </template>
                    </Button>
                </div>
            </CardContent>
        </Card>
    </div>

    <Dialog :open="showDialog">
        <DialogContent>
            <DialogHeader>
                <DialogTitle class="tw-text-xl">Profile Updated Successfully!</DialogTitle>
            </DialogHeader>
            <DialogDescription>
                Redirecting Back to Home Page...
            </DialogDescription>
        </DialogContent>
    </Dialog>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getFirestore, doc, getDoc, updateDoc } from 'firebase/firestore'
import { getAuth, onAuthStateChanged } from 'firebase/auth'
import { Loader2 } from 'lucide-vue-next'
import { useRouter } from 'vue-router' // Import useRouter


import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Dialog, DialogHeader, DialogContent, DialogTitle, DialogDescription, DialogClose, DialogFooter } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'

// State
const loading = ref(true)
const saving = ref(false)
const profileData = ref({
    userType: 'supplier',
    companyName: '',
    companyDescription: ''
})
const showDialog = ref(false);

const auth = getAuth()
const db = getFirestore()
const router = useRouter()  // Initialize router


const loadUserData = async (user) => {
    if (!user) return

    try {
        const docRef = doc(db, 'users', user.uid)
        const docSnap = await getDoc(docRef)

        if (docSnap.exists()) {
            const data = docSnap.data()
            profileData.value = {
                userType: data.userType || 'supplier',
                companyName: data.companyName || '',
                companyDescription: data.companyDescription || ''
            }
        }
    } catch (err) {
        console.error('Failed to load profile data:', err)
    } finally {
        loading.value = false
    }
}


const handleSubmit = async () => {
    saving.value = true

    try {
        const user = auth.currentUser
        if (!user) return

        if (profileData.value.userType == "supplier") {
            const docRef = doc(db, 'users', user.uid)
            await updateDoc(docRef, {
                companyName: profileData.value.companyName,
                companyDescription: profileData.value.companyDescription,
            })
        } else {
            const docRef = doc(db, 'users', user.uid)
            await updateDoc(docRef, {
                companyName: profileData.value.companyName,
                companyDescription: null,
            })
        }
        showDialog.value = true

        setTimeout(() => {
            showDialog.value = false
            router.push('/');
        }, 1000)

    } catch (err) {
        console.error('Failed to update profile:', err)
    } finally {
        saving.value = false
    }
}


onMounted(() => {
    onAuthStateChanged(auth, (user) => {
        if (user) {
            console.log(user)
            loadUserData(user)
        } else {
            loading.value = false
        }
    })
})
</script>