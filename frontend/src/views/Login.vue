<script setup>
import Footer from '@/components/Footer.vue';
import Header from '@/components/Header.vue';
import { loginComposable } from '@/composables/useSegurancaComposable';
import { loginSchema } from '@/schemas/validacoesSchema';
import { Form, Field, ErrorMessage } from 'vee-validate';
import { ref } from 'vue';

let botao = ref('block');
let preloader = ref('none');

let email = ref('');
let password = ref('');
const { sendData } = loginComposable();
let enviar = () => {
    botao.value = 'none';
    preloader.value = 'block';
    sendData({ email: email.value, password: password.value });
};
</script>

<template>
    <Header />
    <div className="breadcumb-area bg-img bg-overlay" style="background-image: url(img/bg-img/breadcumb6.jpg)">
        <div className="container h-100">
            <div className="row h-100 align-items-center">
                <div className="col-12">
                    <div className="breadcumb-text text-center">
                        <h2>Login</h2>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div className="contact-area section-padding-0-80">
        <div className="container">
            <div className="row">
                <div className="col-12">
                    <div className="section-heading">
                        <h3>Insira seus dados</h3>
                    </div>
                </div>
            </div>

            <div className="row">
                <div className="col-8">
                    <div className="contact-form-area">
                        <Form :validation-schema="loginSchema" @submit="enviar()">

                            <div class="row">

                                <div class="col-12 col-lg-12">
                                    <ErrorMessage name="email" class="text text-danger" />
                                    <Field type="text" name="email" v-model="email" class="form-control"
                                        placeholder="Email:" />
                                </div>

                                <div class="col-12 col-lg-12">
                                    <ErrorMessage name="password" class="text text-danger" />
                                    <Field type="password" v-model="password" name="password" class="form-control"
                                        placeholder="Contraseña:" />
                                </div>

                                <div class="col-12 text-center" :style="'display:' + botao">
                                    <button class="btn delicious-btn mt-30" type="submit" title="Enviar">
                                        Enviar
                                    </button>
                                </div>
                                <div class="col-12 text-center" :style="'display:' + preloader">
                                    <img src="/img/img/load.gif" />
                                </div>

                            </div>
                        </Form>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <Footer />
</template>