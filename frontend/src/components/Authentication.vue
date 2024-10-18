<script setup>
import Navbar from './Navbar.vue';
import { auth, db } from '../firebase.js';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, updateProfile } from "firebase/auth";
import { setDoc, doc } from 'firebase/firestore';
import { Card , CardHeader, CardContent, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select } from "@/components/ui/select";
</script>

<!-- HTML STUFF -->
<template>
    <Navbar />
    <div>
        <Card class="tw-w-[350px]">
            <CardHeader>
                <CardTitle>Create project</CardTitle>
                <CardDescription>Deploy your new project in one-click.</CardDescription>
            </CardHeader>
            <CardContent>
                <form>
                    <div class="tw-grid tw-items-center tw-w-full tw-gap-4">
                        <div class="tw-flex tw-flex-col tw-space-y-1.5">
                            <Label for="name">Name</Label>
                            <Input id="name" placeholder="Name of your project" />
                        </div>
                        <div class="tw-flex tw-flex-col tw-space-y-1.5">
                            <Label for="framework">Framework</Label>
                            <Select>
                                <SelectTrigger id="framework">
                                    <SelectValue placeholder="Select" />
                                </SelectTrigger>
                                <SelectContent position="popper">
                                    <SelectItem value="nuxt">
                                        Nuxt
                                    </SelectItem>
                                    <SelectItem value="next">
                                        Next.js
                                    </SelectItem>
                                    <SelectItem value="sveltekit">
                                        SvelteKit
                                    </SelectItem>
                                    <SelectItem value="astro">
                                        Astro
                                    </SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                    </div>
                </form>
            </CardContent>
            <CardFooter class="tw-flex tw-justify-between tw-px-6 tw-pb-6">
                <Button variant="outline">
                    Cancel
                </Button>
                <Button>Deploy</Button>
            </CardFooter>
        </Card>
    </div>
    <div class="login-container">
        <form @submit.prevent="handleLogin" v-if="isLogin">
            <h1> 🔒 Login</h1>
            <div class="form-group">
                <label for="email">Email </label>
                <input type="email" id="email" v-model="email" placeholder="Enter your email" required />
            </div>

            <div class="form-group">
                <label for="password">Password </label>
                <input type="password" id="password" v-model="password" placeholder="Enter your password" required />
            </div>
            <button class="button-submit" type="submit">Log In</button>
        </form>

        <form @submit.prevent="handleSignUp" v-else>
            <h1> 📋 Sign Up</h1>
            <div class="form-group">
                <label for="email">User Type </label>
                <div class="btn-group w-100">
                    <button type="button" class="btn"
                        :class="{ 'btn-primary': !isSupplier, 'btn-outline-primary': isSupplier }"
                        @click="isSupplier = false">Restaurant</button>
                    <button type="button" class="btn"
                        :class="{ 'btn-primary': isSupplier, 'btn-outline-primary': !isSupplier }"
                        @click="isSupplier = true">Supplier</button>
                </div>
            </div>
            <div class="form-group">
                <label for="email">Name </label>
                <input type="text" v-model="userName" placeholder="Enter your username" required />
            </div>

            <div class="form-group">
                <label for="email">Email </label>
                <input type="email" id="email" v-model="email" placeholder="Enter your email" required />
            </div>

            <div class="form-group">
                <label for="password">Password </label>
                <input type="password" id="password" v-model="password" placeholder="Enter your password" required />
            </div>

            <button class="button-submit" type="submit">Sign Up</button>
        </form>

        <button class="d-inline button-switch" @click="toggleLogin">{{ switchLabel }}</button>
    </div>
</template>

<!-- VUE STUFF -->
<script>
export default {
    name: 'Authentication',
    data() {
        return {
            email: '',
            password: '',
            userName: '',
            isLogin: true,
            isSupplier: false,
            switchLabel: "Don't have an account? Sign Up Instead",
        };
    },
    methods: {
        toggleLogin() {
            this.isLogin = !this.isLogin;
            if (this.isLogin) {
                this.switchLabel = "Don't have an account? Sign Up Instead"
            } else {
                this.switchLabel = 'Already have an account? Log In Instead'
            }

        },
        handleLogin() {
            signInWithEmailAndPassword(auth, this.email, this.password)
                .then((userCredential) => {
                    alert("Signed In")
                    // Signed in -> Redirect to home page
                    const user = userCredential.user;
                    this.$router.push('/');
                })
                .catch((error) => {
                    // Wrong password
                    alert("Wrong Username/Password. Try Again!")
                    const errorCode = error.code;
                    const errorMessage = error.message;
                });
        },
        handleSignUp() {
            // Check if userName is taken
            createUserWithEmailAndPassword(auth, this.email, this.password)
                .then((userCredential) => {
                    // Signed up + Store UserName
                    const user = userCredential.user;
                    updateProfile(user, {
                        displayName: this.userName
                    })

                    // Add user data into firebase DB (Username + Account Type + Points )
                    // Store additional data in Firestore
                    setDoc(doc(db, "users", user.uid), {
                        userName: this.userName,
                        userType: this.isSupplier ? "supplier" : "restaurant",
                        points: this.isSupplier ? null : 0,
                    })
                        .then(() => {
                            alert("User signed up");
                            this.$router.push('/');
                        })
                        .catch((error) => {
                            console.error("Error adding document: ", error);
                        }
                        )
                })
                .catch((error) => {
                    console.error("Error in Signing Up, Please Try Again!", error)
                    // ..
                });
        }
    }
};
</script>

<!-- CSS STUFF -->
<style>
.login-container {
    width: 80%;
    max-width: 500px;
    margin: 20px auto;
    padding: 20px;
    background-color: white;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
    margin-bottom: 15px;
}

.button-submit {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-bottom: 10px;
}

.button-switch {
    width: 100%;
    padding: 10px;
    background-color: #ebebeb;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

h1 {
    text-align: center;
    margin-bottom: 20px;
}

input {
    width: 100%;
    padding: 10px;
    margin-top: 5px;
    border: 1px solid #ccc;
    border-radius: 10px;
}
</style>