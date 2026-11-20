package com.nplstudio.tts

import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query

/**
 * NPL Studio's app-to-backend contract.
 *
 * These are YOUR backend routes, not CapCut endpoints. The backend must use
 * a permitted/authorized provider integration and keep any session secrets
 * off the Android client.
 */
interface CapCutTtsGateway {
    @GET("v1/tts/voices")
    suspend fun listVoices(
        @Query("language") language: String = "vi-VN"
    ): VoiceCatalogResponse

    @POST("v1/tts/jobs")
    suspend fun createJob(
        @Body request: CreateTtsJobRequest
    ): TtsJobResponse

    @GET("v1/tts/jobs/{jobId}")
    suspend fun getJob(
        @Path("jobId") jobId: String
    ): TtsJobResponse
}

data class VoiceCatalogResponse(
    val voices: List<VoiceItem>,
    val updatedAt: String? = null
)

data class VoiceItem(
    val id: String,
    val displayName: String,
    val language: String,
    val voiceType: String,
    val previewUrl: String? = null,
    val availability: String = "unknown"
)

data class CreateTtsJobRequest(
    val text: String,
    val voiceId: String,
    val language: String = "vi-VN",
    val rate: Float = 1.0f,
    val projectId: String? = null,
    val cueStartMs: Long? = null,
    val cueEndMs: Long? = null
)

data class TtsJobResponse(
    val jobId: String,
    val status: String, // queued | processing | succeeded | failed
    val audioUrl: String? = null,
    val errorCode: String? = null,
    val message: String? = null
)
