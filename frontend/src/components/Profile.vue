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

                        <div class="space-y-2">
                            <Label for="companyAddress">Company Address</Label>
                            <Input id="companyAddress" v-model="profileData.companyAddress" :disabled="saving"
                                :placeholder="profileData.companyAddress || 'Enter company address...'" />
                        </div>

                        <div class="space-y-2">
                            <Label for="companyAddress">Company Number</Label>
                            <Input id="companyAddress" v-model="profileData.companyNumber" :disabled="saving"
                                :placeholder="profileData.companyNumber || 'Enter company number...'" />
                        </div>

                        <div v-if="profileData.userType === 'supplier'" class="space-y-2">
                            <Label for="companyDescription">Company Description</Label>
                            <Textarea id="companyDescription" v-model="profileData.companyDescription" rows="4"
                                :disabled="saving"
                                :placeholder="profileData.companyDescription || 'Describe your business...'" />
                        </div>
                    </div>

                    <div v-if="profileData.userType === 'supplier'" class="space-y-2">
                        <Label>Company Logo</Label>
                        <div class="space-y-2">
                            <img 
                                v-if="imagePreview" 
                                :src="imagePreview" 
                                alt="Company Logo" 
                                class="w-32 h-32 object-cover rounded-lg"
                            />
                            <input 
                                type="file" 
                                accept="image/*" 
                                @change="handleImageUpload" 
                                class="mt-1 block w-full text-sm text-gray-500
                                file:mr-4 file:py-2 file:px-4
                                file:rounded-full file:border-0
                                file:text-sm file:font-semibold
                                file:bg-blue-50 file:text-blue-700
                                hover:file:bg-blue-100"
                            />
                        </div>
                    </div>

                    <div class="space-y-4">
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
                </div>
            </CardContent>
        </Card>

        <!-- Success Dialog -->
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

        <!-- Delete Account Dialog -->
        <AlertDialog :open="showDeleteDialog">
            <AlertDialogContent>
                <AlertDialogHeader>
                    <AlertDialogTitle>
                        <div class="flex items-center gap-2">
                            <AlertTriangle class="h-5 w-5 text-red-500" />
                            Delete Account
                        </div>
                    </AlertDialogTitle>
                    <AlertDialogDescription>
                        Are you sure you want to delete your account? This action cannot be undone and all your data will be
                        permanently removed.
                    </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                    <AlertDialogCancel @click="showDeleteDialog = false">
                        Cancel
                    </AlertDialogCancel>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>

        <ImageCropper
            v-if="showCropper && selectedFile"
            :image-file="selectedFile"
            @crop-complete="handleCropComplete"
            @cancel="() => showCropper = false"
        />
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { getFirestore, doc, getDoc, updateDoc, deleteDoc } from 'firebase/firestore'
import { getAuth, onAuthStateChanged, deleteUser } from 'firebase/auth'
import { Loader2, AlertTriangle } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import {
    Dialog,
    DialogHeader,
    DialogContent,
    DialogTitle,
    DialogDescription
} from '@/components/ui/dialog'
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import ImageCropper from './Supplier/ImageCropper.vue'
import 'vue-advanced-cropper/dist/style.css'

// State
const loading = ref(true)
const saving = ref(false)
const showDialog = ref(false)
const showDeleteDialog = ref(false)
const profileData = ref({
    userType: 'supplier',
    companyName: '',
    companyDescription: '',
    companyNumber: ''
})

const auth = getAuth()
const db = getFirestore()
const router = useRouter()

const showCropper = ref(false)
const selectedFile = ref(null)
const imageFile = ref(null)
const imagePreview = ref('')

const handleImageUpload = (event) => {
    const file = event.target.files[0]
    if (file) {
        selectedFile.value = file
        showCropper.value = true
    }
}

const fileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = () => resolve(reader.result)
        reader.onerror = error => reject(error)
    })
}

const handleCropComplete = ({ file, url }) => {
    imageFile.value = file
    imagePreview.value = url
    showCropper.value = false
}

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
                companyAddress: data.companyAddress || '',
                companyDescription: data.companyDescription || '',
                companyNumber: data.companyNumber || ''
            }
            if (data.imageData) {
                imagePreview.value = data.imageData
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

        let updateData = {
            companyName: profileData.value.companyName,
            companyAddress: profileData.value.companyAddress,
            companyNumber: profileData.value.companyNumber,
        }

        if (profileData.value.userType === "supplier") {
            updateData.companyDescription = profileData.value.companyDescription
            if (imageFile.value) {
                const base64Image = await fileToBase64(imageFile.value)
                updateData.imageData = base64Image
            }
        }

        const docRef = doc(db, 'users', user.uid)
        await updateDoc(docRef, updateData)

        showDialog.value = true
        setTimeout(() => {
            showDialog.value = false
            router.push('/')
        }, 1000)

    } catch (err) {
        console.error('Failed to update profile:', err)
    } finally {
        saving.value = false
    }
}

// const handleDeleteAccount = async () => {
//     saving.value = true
//     try {
//         const user = auth.currentUser
//         if (!user) return

//         // Delete the user's document from Firestore
//         const userDoc = doc(db, 'users', user.uid)
//         await deleteDoc(userDoc)

//         // Delete the user's authentication account
//         await deleteUser(user)

//         // Close the dialog and navigate to login page
//         showDeleteDialog.value = false
//         router.push('/login')
//     } catch (err) {
//         console.error('Failed to delete account:', err)
//         // You might want to show an error message to the user here
//     } finally {
//         saving.value = false
//     }
// }

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

onBeforeUnmount(() => {
    if (imagePreview.value) {
        URL.revokeObjectURL(imagePreview.value)
    }
})
</script>