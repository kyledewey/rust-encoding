// AUTOGENERATED FROM index-iso-8859-4.txt, ORIGINAL COMMENT FOLLOWS:
//
// Any copyright is dedicated to the Public Domain.
// http://creativecommons.org/publicdomain/zero/1.0/
//
// For details on index-iso-8859-4.txt see the Encoding Standard
// http://encoding.spec.whatwg.org/

static FORWARD_TABLE: &'static [u16] = &[
    128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142,
    143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157,
    158, 159, 160, 260, 312, 342, 164, 296, 315, 167, 168, 352, 274, 290, 358,
    173, 381, 175, 176, 261, 731, 343, 180, 297, 316, 711, 184, 353, 275, 291,
    359, 330, 382, 331, 256, 193, 194, 195, 196, 197, 198, 302, 268, 201, 280,
    203, 278, 205, 206, 298, 272, 325, 332, 310, 212, 213, 214, 215, 216, 370,
    218, 219, 220, 360, 362, 223, 257, 225, 226, 227, 228, 229, 230, 303, 269,
    233, 281, 235, 279, 237, 238, 299, 273, 326, 333, 311, 244, 245, 246, 247,
    248, 371, 250, 251, 252, 361, 363, 729,
];

#[inline]
pub fn forward(code: u8) -> u16 {
    FORWARD_TABLE[code as uint]
}

#[inline]
pub fn backward(code: u16) -> u8 {
    match code {
        128 => 0, 129 => 1, 130 => 2, 131 => 3, 132 => 4, 133 => 5, 134 => 6,
        135 => 7, 136 => 8, 137 => 9, 138 => 10, 139 => 11, 140 => 12,
        141 => 13, 142 => 14, 143 => 15, 144 => 16, 145 => 17, 146 => 18,
        147 => 19, 148 => 20, 149 => 21, 150 => 22, 151 => 23, 152 => 24,
        153 => 25, 154 => 26, 155 => 27, 156 => 28, 157 => 29, 158 => 30,
        159 => 31, 160 => 32, 260 => 33, 312 => 34, 342 => 35, 164 => 36,
        296 => 37, 315 => 38, 167 => 39, 168 => 40, 352 => 41, 274 => 42,
        290 => 43, 358 => 44, 173 => 45, 381 => 46, 175 => 47, 176 => 48,
        261 => 49, 731 => 50, 343 => 51, 180 => 52, 297 => 53, 316 => 54,
        711 => 55, 184 => 56, 353 => 57, 275 => 58, 291 => 59, 359 => 60,
        330 => 61, 382 => 62, 331 => 63, 256 => 64, 193 => 65, 194 => 66,
        195 => 67, 196 => 68, 197 => 69, 198 => 70, 302 => 71, 268 => 72,
        201 => 73, 280 => 74, 203 => 75, 278 => 76, 205 => 77, 206 => 78,
        298 => 79, 272 => 80, 325 => 81, 332 => 82, 310 => 83, 212 => 84,
        213 => 85, 214 => 86, 215 => 87, 216 => 88, 370 => 89, 218 => 90,
        219 => 91, 220 => 92, 360 => 93, 362 => 94, 223 => 95, 257 => 96,
        225 => 97, 226 => 98, 227 => 99, 228 => 100, 229 => 101, 230 => 102,
        303 => 103, 269 => 104, 233 => 105, 281 => 106, 235 => 107, 279 => 108,
        237 => 109, 238 => 110, 299 => 111, 273 => 112, 326 => 113, 333 => 114,
        311 => 115, 244 => 116, 245 => 117, 246 => 118, 247 => 119, 248 => 120,
        371 => 121, 250 => 122, 251 => 123, 252 => 124, 361 => 125, 363 => 126,
        729 => 127, _ => 255
    }
}

#[cfg(test)]
mod tests {
    use std::u8;
    use super::{forward, backward};

    #[test]
    fn test_correct_table() {
        for u8::range(0, 128) |i| {
            let j = forward(i);
            if j != 0xffff { assert_eq!(backward(j), i); }
        }
    }
}